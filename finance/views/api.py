import django.db
from django.db.models import Sum
from django.http import Http404
from rest_framework import filters, viewsets
from rest_framework.decorators import action, link
from rest_framework import exceptions
from rest_framework.response import Response

import finance.filters
from finance import models
from finance import serializers


class AccountViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Provides /accounts, /accounts/:id, and /accounts/:id/transactions
    """
    queryset = models.Account.objects.all()
    serializer_class = serializers.AccountSerializer

    @link()
    def transactions(self, request, format=None, pk=None):
        if pk:
            request.GET = {"account": pk}
            return TransactionViewSet.as_view(actions={"get": "list"})(request, format=format)
        else:
            raise Http404()

    @action()
    def sync(self, request, format=None, pk=None):
        account = self.get_object()
        new_trx = account.sync()
        return Response([serializers.TransactionSerializer(t).data for t in new_trx])


class InstitutionViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = models.Institution.objects.all()
    serializer_class = serializers.InstitutionSerializer


class TransactionViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Provides /transactions (with optional account and order_by params), and /transactions/:id
    """
    queryset = models.Transaction.objects.all()
    serializer_class = serializers.TransactionSerializer
    filter_backends = (filters.OrderingFilter, filters.DjangoFilterBackend)
    filter_fields = ("account",)


class StatsViewSet(viewsets.ViewSet):
    def _filtered_stats(self, request, interval):
        truncate_date = django.db.connection.ops.date_trunc_sql(interval, "date")
        query = models.Transaction.objects.extra({interval: truncate_date})\
            .values(interval).annotate(total_amount=Sum("amount")).order_by(interval)
        # TODO: Filter query with user ID
        # TODO: Should require account_id in most cases
        return finance.filters.StatsFilter(request.GET, queryset=query).qs

    VALID_INTERVALS = ("day", "month", "year")

    def list(self, request):
        interval = request.QUERY_PARAMS.get("interval", "day")
        if not interval in self.VALID_INTERVALS:
            raise exceptions.ParseError("interval must be one of: %s" % ", ".join(self.VALID_INTERVALS))

        query = self._filtered_stats(request, interval)
        return Response({
            "deposits": query.filter(amount__gte=0),
            "withdrawals": query.filter(amount__lt=0)
        })


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer


class CategoryRuleViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.CategoryRule.objects.all()
    serializer_class = serializers.CategoryRuleSerializer
