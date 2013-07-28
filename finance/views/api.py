import django.db
from django.db.models import Sum
from rest_framework import generics, viewsets
from rest_framework.decorators import link
from rest_framework.fields import SerializerMethodField
from rest_framework.response import Response
from rest_framework.views import APIView

from finance.models import Account, Institution, Transaction
from finance.serializers import AccountSerializer, InstitutionSerializer, TransactionSerializer




class AccountViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = Account.objects.all()
    serializer_class = AccountSerializer


class InstitutionSerializer(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = Institution.objects.all()
    serializer_class = InstitutionSerializer


class TransactionViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer


class StatsViewSet(viewsets.ViewSet):
    def list(self, request, format=None ):
        truncate_date = django.db.connection.ops.date_trunc_sql("day", "date")
        query = Transaction.objects.extra({"day": truncate_date}).values("day").annotate(total_amount=Sum("amount")).order_by("day")
        return Response({
            "deposits": query.filter(amount__gte=0),
            "withdrawals": query.filter(amount__lt=0)
        })
