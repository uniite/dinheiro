import django.db
from django.db.models import Sum
from django.http import Http404
import django_filters
from rest_framework import generics, filters, viewsets
from rest_framework.decorators import action, link
from rest_framework.fields import SerializerMethodField
from rest_framework.response import Response
from rest_framework.views import APIView

from finance.models import Account, Institution, Transaction
from finance.serializers import AccountSerializer, InstitutionSerializer, TransactionSerializer


class TransactionsFilter(django_filters.FilterSet):
    class Meta:
        model = Transaction
        fields = ["account"]

class StatsFilter(django_filters.FilterSet):
    min_amount = django_filters.NumberFilter("amount", lookup_type="gte")
    max_amount = django_filters.NumberFilter("amount", lookup_type="lte")

    class Meta:
        model = Transaction
        fields = ["account", "amount", "category", "currency", "date", "payee"]


class AccountViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Provides /accounts, /accounts/:id, and /accounts/:id/transactions
    """
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

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
        return Response([TransactionSerializer(t).data for t in new_trx])


class InstitutionSerializer(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = Institution.objects.all()
    serializer_class = InstitutionSerializer


class TransactionViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Provides /transactions (with optional account and order_by params), and /transactions/:id
    """
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    filter_backends = (filters.OrderingFilter, filters.DjangoFilterBackend)
    filter_fields = ("account",)


class StatsViewSet(viewsets.ViewSet):
    def list(self, request, format=None):
        truncate_date = django.db.connection.ops.date_trunc_sql("day", "date")
        query = Transaction.objects.extra({"day": truncate_date}).values("day").annotate(total_amount=Sum("amount")).order_by("day")
        # TODO: Filter query with user ID
        # TODO: Should require account_id in most cases
        query = StatsFilter(request.GET, queryset=query).qs
        return Response({
            "deposits": query.filter(amount__gte=0),
            "withdrawals": query.filter(amount__lt=0)
        })
