from collections import defaultdict
import time

import django.db
import numpy
from django.db.models import Sum
from django.http import Http404
from django_pandas.io import read_frame
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
        return Response({
            "transactions": [serializers.TransactionSerializer(t).data for t in new_trx],
            "balance": models.Account.objects.get(pk=account.pk).balance
        })


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


class SummaryStatsViewSet(viewsets.ViewSet):
    def _filtered_stats(self, request, sum_by=None, average_by=None):
        query = models.Transaction.objects
        # TODO: Filter query with user ID
        # TODO: Should require account_id in most cases
        # Apply general filters (eg. by amount or category)
        query = finance.filters.StatsFilter(request.GET, queryset=query).qs
        # Sum the transaction amounts by the given field
        if sum_by:
            # query.extra({sum_by: truncate_date}).values("day").annotate(total_amount=Sum("amount")).order_by("day")
            truncate_date = django.db.connection.ops.date_trunc_sql(sum_by, "date")
            query = query.extra({sum_by: truncate_date})\
                .values(sum_by).annotate(total_amount=Sum("amount")).order_by(sum_by)
        # Average the amounts (or sums) by the given criteria (day_of_week or month)
        if average_by:
            if average_by == "day_of_week":
                # Sums by day of week
                dow_sums = defaultdict(int)
                for t in query:
                    # Add the transaction's amount to the correct day of the week
                    dow = time.strptime(t["day"], "%Y-%m-%d %H:%M:%S").tm_wday
                    dow_sums[dow] += t.amount
                # Calculate and return the average

        # Default is to return the query as-is
        return query


    VALID_INTERVALS = ("day", "month", "year")

    def list(self, request):
        sum_by = request.QUERY_PARAMS.get("sum_by", "day")
        if not sum_by in self.VALID_INTERVALS:
            raise exceptions.ParseError("sum_by must be one of: %s" % ", ".join(self.VALID_INTERVALS))
        average_by = request.QUERY_PARAMS.get("average_by")
        if average_by:
            if average_by in ("day", "day_of_week", "month"):
                query = query.annotate()

        query = self._filtered_stats(request, sum_by, average_by)
        return Response({
            "deposits": query.filter(amount__gte=0),
            "withdrawals": query.filter(amount__lt=0)
        })


class StatsViewSet(viewsets.ViewSet):
    def list(self, request):
        stats_by = request.GET.get('by', 'category')

        original_df = read_frame(models.Transaction.objects.filter(amount__lt=0).exclude(category__name='Credit Card Payments'),
                                 fieldnames=['date', 'category', 'amount'])
        df = original_df.set_index('date').groupby('category').resample('M', how='sum')

        chart_df = df.reset_index()\
                     .pivot_table(values='amount', index=['date'], columns=['category'], aggfunc=numpy.sum)\
                     .replace(numpy.NaN, 0)

        months = [x.strftime('%Y-%m-%d') for x in chart_df.index]
        chart_series = [
            {'name': category, 'type': 'column', 'data': [abs(float(a)) for a in amounts]}
            for category,amounts in chart_df.iteritems()]

        table_data = [{'category': category, 'amounts': list(amounts)} for category,amounts in chart_df.iteritems()]
        total_df = original_df.set_index('date').resample('M', how='sum').transpose()
        table_data.append(({'category': 'Total', 'amounts': total_df.values[0]}))

        return Response({
            'months': months,
            'series': chart_series,
            'table_data': table_data,
        })


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer


class CategoryRuleViewSet(viewsets.ModelViewSet):
    queryset = models.CategoryRule.objects.all()
    serializer_class = serializers.CategoryRuleSerializer
