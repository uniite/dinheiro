import datetime
from decimal import Decimal
from StringIO import StringIO

from django.db import models
from django.core import validators
from django.utils import timezone

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

    fid = models.IntegerField()
    org = models.CharField(max_length=50)
    url = models.CharField(max_length=255)
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=128)
    # The name of the institution (from OFXHome or similar)
    name = models.CharField(max_length=255, default="Unknown")

    class Meta:
        unique_together = ("fid", "username")


    def clean(self):
        self.name = self.name.strip()
        self.org = self.org.strip()
        self.url = self.url.strip()


    def sync(self):
        """
        Synchronizes accounts with financial data retrieved using the instition's OFX API.

        :returns: The number of transactions added.
        """

        ofx_inst = ofxclient.Institution(str(self.fid), self.org, self.url, self.username, self.password)

        added_transactions = 0

        # Retrieve a list of the remote instiitution's accounts
        for ofx_account in ofx_inst.accounts():
            # If we don't have a copy of the account locally, create it
            # TODO: Detect accounts with changed account numbers (eg. a re-issued credit card)
            local_account, created = self.account_set.get_or_create(account_number=ofx_account.number)
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
                # Validate and save
                local_transaction.full_clean()
                # TODO: Make it validate transaction_id uniqueness down here (less work for the DB)
                local_transaction.save()
                added_transactions += 1

        return added_transactions


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
    name = models.CharField(max_length=50)

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
    # The type of trasnsaction (eg. "debit")
    type = models.CharField(blank=True, max_length=50)

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
