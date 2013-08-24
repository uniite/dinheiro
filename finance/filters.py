import django_filters

from finance import models


class TransactionsFilter(django_filters.FilterSet):
    class Meta:
        model = models.Transaction
        fields = ["account"]


class StatsFilter(django_filters.FilterSet):
    min_amount = django_filters.NumberFilter("amount", lookup_type="gte")
    max_amount = django_filters.NumberFilter("amount", lookup_type="lte")

    class Meta:
        model = models.Transaction
        fields = ["account", "amount", "category", "currency", "date", "payee"]
