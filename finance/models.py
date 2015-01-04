import datetime
from collections import defaultdict
from decimal import Decimal
from StringIO import StringIO

from django.contrib.auth.models import User
from django.db import models
from django.core import validators
from django.utils import timezone
from django.dispatch import receiver

import ofxclient
from ofxclient.client import Client
from ofxparse import OfxParser
from BeautifulSoup import BeautifulStoneSoup



"""
OFXClient notes:
An ofxclient.Acccount has:
        type
        account_id/number
        routing_number
        account_type
        type
        watnings
        institution

An ofxclient.statement has:
        available_balance
        balance
        currency
        discarded_entries
        end_date
        start_date
        transactions
        warnings
An ofxclient statement transaction has:
        payee
        type
        date
        amount
        id
        memo
        sic  #
        mcc  # Merchant category code: https://code.google.com/p/ofx-parser/source/browse/trunk/lib/mcc.rb?r=5
"""

# The default/initial number of days back to sync for Transactions
# TODO: Put this in some config?
DEFAULT_SYNC_DAYS = 90


class Institution(models.Model):
    """
    An online account at a financial institution.

    Note that no financial information is stored here (see Account).
    """

    owner = models.ForeignKey(User)
    # Financial institution ID?
    fid = models.IntegerField()
    # Some sort of OFX organization ID
    org = models.CharField(max_length=50)
    # OFX API endpoint
    url = models.CharField(max_length=255)
    # Credentials (careful, these are the user's online banking credentials)
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=128)
    # The name of the institution (from OFXHome or user-defined)
    name = models.CharField(max_length=255, default="Unknown")

    class Meta:
        unique_together = ("fid", "username")

    def clean(self):
        self.name = self.name.strip()
        self.org = self.org.strip()
        self.url = self.url.strip()

    def sync(self):
        """
        Synchronizes accounts with financial data retrieved using the institution's OFX API.

        :returns: A list of new :pytype:Transaction objects.
        """

        ofx_inst = ofxclient.Institution(str(self.fid), self.org, self.url, self.username, self.password)

        new_transactions = []

        # Retrieve a list of the remote institution's accounts
        ofx_accounts = ofx_inst.accounts()
        # Something is wrong if we couldn't find any accounts...
        if not ofx_accounts:
            raise Exception("Could not retrieve account information. "
                            "This usually means your password has changed or your account is locked.")
        # Process each account found via OFX
        for ofx_account in ofx_accounts:
            # If we don't have a copy of the account locally, create it
            # TODO: Detect accounts with changed account numbers (eg. a re-issued credit card)
            local_account, created = self.account_set.get_or_create(account_number=ofx_account.number)
            local_account.name = self.name
            # Try to figure out how far back to sync
            if local_account.transaction_set.exists():
                # We already have some Transactions; sync up through the day before the newest Transaction
                # (this ensures we catch Transactions from Institutions that have poor date accuracy)
                last_transaction_date = local_account.transaction_set.order_by("-date")[0].date
                sync_days = (timezone.now() - last_transaction_date).days + 1
                # Limit it based on the default
                sync_days = min(sync_days, DEFAULT_SYNC_DAYS)
            else:
                # We don't have any Transactions yet; sync the default amount
                sync_days = DEFAULT_SYNC_DAYS

            # Sync this Account by downloading an account statement
            # TODO: Determine what amount of days is a good default
            statement = ofx_account.statement(days=sync_days)
            if hasattr(statement, "available_balance"):
                local_account.available_balance = statement.available_balance
            local_account.balance = statement.balance
            # Validate and save (TODO: do the whole sync as a database transaction?)
            local_account.full_clean()
            local_account.save()

            # Sync this statement's transactions with our local records
            for ofx_transaction in statement.transactions:
                # Skip the transaction if we already have it
                # TODO: I have no idea if transactions IDs are enforced by the spec
                if local_account.transaction_set.filter(transaction_id=ofx_transaction.id).exists():
                    continue
                # Create a new local Transaction based on the OFX data
                local_transaction = Transaction(
                        account=local_account,
                        amount=Decimal(ofx_transaction.amount),
                        currency=statement.currency,
                        transaction_id = ofx_transaction.id,
                )
                # Copy over some attributes that map 1:1 with our local Transaction model
                for attr in ("date", "payee", "mcc", "memo", "sic", "type"):
                    setattr(local_transaction, attr, getattr(ofx_transaction, attr))
                    # Fix up some escaped characters
                    local_transaction.payee = local_transaction.payee.replace("&amp;", "&")
                # Validate and save
                local_transaction.full_clean()
                # TODO: Make it validate transaction_id uniqueness down here (less work for the DB)
                local_transaction.save()
                new_transactions.append(local_transaction)

        # Categorize all the new transactions
        # TOOD: Do it on these instead of on all
        for c in Category.objects.all():
            c.apply()

        return new_transactions


number_validator = validators.RegexValidator(r"^\d+$", "Must be a number")
class Account(models.Model):
    """
     A financial account belonging to an institution, and contains basic account information.

    Note that no account credentials are stored here (see Institution).
    """

    institution = models.ForeignKey(Institution)
    # Account numbers are not integers, because they can be of arbitrary length,
    # they aren't normally used in mathematical operations (except checksums),
    # and they might contain letters in special cases (in which case we can just change the validator)
    account_number = models.CharField(max_length=50, validators=[number_validator])
    # User-defined name for the account, to identify it (since we don't want to toss around the account number)
    name = models.CharField(max_length=50, blank=True)

    ## Optional fields
    # Same goes for routing number (although I'm not sure about the length)
    routing_number = models.CharField(blank=True, max_length=9, validators=[number_validator])
    # Remember kids, always use Decimal for monetary amounts
    balance = models.DecimalField(decimal_places=2, max_digits=15, default=0)
    # Not sure what this is for, but ofxclient is aware of it
    broker_id = models.CharField(blank=True, max_length=50)

    class Meta:
        unique_together = ("institution", "account_number")

    def censored_account_number(self):
        """ The account number with all but the last four (or less) digits censored. """
        # (eg. "1234" => "***4", "12345678910" => "*******8910")
        show_digits = max(4, len(self.account_number) // 2.5)
        return ((len(self.account_number) - 4) * "*") + self.account_number[-4:]

    def sync(self):
        """
        TODO: Currently it is just an alias for institution.sync
        (which syncs all the institution's accounts)
        """
        return self.institution.sync()

    def find_recurring_transactions(self):
        trx = Transaction.objects.filter(account=self)
        # First, build the dict index
        # Structure: {'2014-03': {'Payee': 4, ...}, ...}
        monthly_payee_trx = defaultdict(lambda: defaultdict(list))
        for t in trx:
            monthly_payee_trx[t.date.strftime('%Y-%m')][t.payee].append(t)
        # Then, filter out payees that show up only once a month, and put them in a flattened data structure
        # Structure: {'Payee': [Transaction, ...]}
        recurring_trx = defaultdict(list)
        for month, payee_trx in monthly_payee_trx.iteritems():
            for payee,trx in payee_trx.iteritems():
                if len(trx) == 1:
                    recurring_trx[payee] += trx
        # Finally, filter out transactions that don't happen around the same time each month
        # Note: we use keys instead of iteritems, so we can delete payees in-place
        for payee in recurring_trx.keys():
            # Toss out payees with only one transaction total
            if len(recurring_trx[payee]) == 1:
                recurring_trx.pop(payee)
                continue
            # Get the first date, and ensure every transaction is close to it (+/- 2 days)
            base_date = recurring_trx[payee][0].date
            if not all([abs(base_date.day - t.date.day) <= 2 for t in recurring_trx[payee]]):
                recurring_trx.pop(payee)
            else:
                print "%s, %s" % (payee, len(recurring_trx[payee]))

        return recurring_trx


four_digit_validators = [validators.MinValueValidator(0), validators.MaxValueValidator(4)]
class Transaction(models.Model):
    """ A financial transaction, belonging to an account. """

    account = models.ForeignKey(Account)
    # The amount involved, in the transaction's currency
    amount = models.DecimalField(decimal_places=2, max_digits=15)
    # TODO: Make this a some sort of constant-based integer or ForeignKey
    currency = models.CharField(max_length=3, validators=[validators.RegexValidator(r"^[a-zA-Z]+$")])
    # Note that some institutions only provide dates with day-accuracy
    # (ie. all transactions on June 1 will be marked as noon on June 1)
    date = models.DateTimeField()
    # Usually the name of the person/merchant/company the payment was sent to
    # The exact format varies by institution
    payee = models.CharField(max_length=255)
    # Instition-specific transaction ID
    # TODO: This may not be required by the OFX spec
    transaction_id = models.CharField(max_length=255)

    ## Optional Fields
    # Useful for categorizing transactions, but not all institutions provde it
    # http://en.wikipedia.org/wiki/Merchant_category_code
    mcc = models.IntegerField(blank=True, null=True, validators=four_digit_validators)
    # Arbitrary memo text. This is usually only for Check or ACH transactions.
    memo = models.TextField(blank=True)
    # Optional
    # http://en.wikipedia.org/wiki/Standard_Industrial_Classification
    sic = models.IntegerField(blank=True, null=True, validators=four_digit_validators)
    # The type of transaction (eg. "debit")
    type = models.CharField(blank=True, max_length=50)

    # User-defined optional fields
    category = models.ForeignKey("Category", blank=True, null=True)

    def clean(self):
        # Have to clean IntegerFields myself, since Django uses int to validate them (which isn't very forgiving)
        for attr in [f.name for f in self._meta.fields if isinstance(f, models.IntegerField)]:
            # Turn blank strings into None
            value = getattr(self, attr)
            if type(value) in (str, unicode):
                if not value.strip():
                    setattr(self, attr, None)

    class Meta:
        ordering = ["-date"]
        get_latest_by = "date"
        unique_together = ("account", "transaction_id")


class Category(models.Model):
    """
    A category for classifying with Transactions, to allow budgeting.
    """
    name = models.CharField(max_length=50)
    parent = models.ForeignKey("self", blank=True, null=True)

    def apply(self):
        """ Apply this category to the Transactions it matches. """
        for t in self.matches():
            t.category = self
            t.save()

    def matches(self):
        """ Find all Transactions that match this category. """
        # Construct a query based on our rules
        query = Transaction.objects
        # This will become a bunch of models.Q instances OR'd together
        conditions = None
        for rule in self.rules.all():
            # These are easy and efficient, because they map directly to Django ORM filters
            if rule.type in ("contains", "startswith", "endswith"):
                # Becomes Q(payee__contains="the coffee shop")
                filter_field = "%s__%s" % (rule.field, rule.type)
                filter = models.Q(**{filter_field: rule.content})
                # It is either the first condition
                if conditions is None:
                    conditions = filter
                # or a subsequent condition (OR'd with the rest)
                else:
                    conditions |= filter
        # If we don't have any rules/conditions, return no matches
        if conditions is None:
            return []
        else:
            return query.filter(conditions)



class CategoryRule(models.Model):
    """
    Represents logic for categorization of Transactions.
    """
    RULE_TYPES = (
        ("contains", "Contains"),
        ("startswith", "Starts With"),
        ("endswith", "Ends With"),
    )
    TRANSACTION_FIELDS = (
        ("date", "Date"),
        ("payee", "Payee"),
        ("type", "Type"),
    )
    # The type of string matching to use (may expand to logic types in the future)
    type = models.CharField(max_length=10, choices=RULE_TYPES, default="contains")
    # The field to match against (in the Transaction)
    field = models.CharField(max_length=20, choices=TRANSACTION_FIELDS, default="payee")
    # Text to match against (may contain logic in the future, for new rule types)
    content = models.TextField()
    # The Category to apply if the matched
    category = models.ForeignKey(Category, related_name="rules")

    def clean(self):
        self.content = self.content.lower().strip()


@receiver(models.signals.post_save, sender=CategoryRule)
def apply_rules(sender, instance, **kwargs):
    instance.category.apply()
