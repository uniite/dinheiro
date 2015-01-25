from django_pandas.io import read_frame
from django.shortcuts import HttpResponse, render_to_response
from django.views.generic import ListView
import json
import numpy

from finance.models import Account, Transaction



class TransactionListView(ListView):
    model = Transaction


class AccountTransactionsListView(ListView):

    def get_queryset(self):
        self.account = get_object_or_404(Account, id=self.args[0])
        return self.account.transaction_set.all()

    def get_context_data(self, **kwargs):
        context = super(AccountTransactionsListView, self).get_context_data(**kwargs)
        context["account"] = self.account
        return context


def stats(request):
    stats_by = request.GET.get('by', 'category')

    original_df = read_frame(Transaction.objects.filter(amount__lt=0).exclude(category__name='Credit Card Payments'),
                             fieldnames=['date', 'category', 'amount'])
    df = original_df.set_index('date').groupby('category').resample('M', how='sum')

    chart_df = df.reset_index()\
                 .pivot_table(values='amount', index=['date'], columns=['category'], aggfunc=numpy.sum)\
                 .replace(numpy.NaN, 0)

    months = [x.strftime('%Y-%m-%d') for x in chart_df.index]
    chart_series = [
        {'name': category, 'type': 'column', 'data': [abs(float(a)) for a in amounts]}
        for category,amounts in chart_df.iteritems()]

    table_df = df.reset_index()\
                 .pivot_table(values='amount', index=['category'], columns=['date'], aggfunc=numpy.sum)\
                 .replace(numpy.NaN, 0)#.reset_index()
    table_data = [(category, list(amounts)) for category,amounts in chart_df.iteritems()]
    total_df = original_df.set_index('date').resample('M', how='sum').transpose()
    table_data.append(('Total', total_df.values[0]))

    return render_to_response('transactions/stats.html', {
        'months_json': json.dumps(months),
        'chart_series_json': json.dumps(chart_series),
        'chart_df': chart_df,
        'months': months,
        'table_data': table_data,
    })
