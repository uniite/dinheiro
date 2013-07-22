from decimal import Decimal

from rest_framework import serializers
from finance.models import Account, Institution, Transaction


class AccountSerializer(serializers.ModelSerializer):
    censored_account_number = serializers.SerializerMethodField("get_censored_account_number")

    class Meta:
        model = Account
        fields = ("id", "censored_account_number", "name")

    def get_censored_account_number(self, account):
        return account.censored_account_number()

class InstitutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Institution
        fields = ("id", "fid", "org", "url", "username")

class TransactionSerializer(serializers.ModelSerializer):
    amount = serializers.SerializerMethodField("get_amount")

    class Meta:
        model = Transaction
        fields = ("id", "amount", "date", "payee", "type")

    def get_amount(self, transaction):
        return transaction.amount.quantize(Decimal("1.00"))
