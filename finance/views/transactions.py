import json

from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponse, render_to_response
from pandas import DataFrame
import numpy

from finance.models import Transaction


@login_required
def stats(request):
    stats_by = request.GET.get('by', 'category')

    trx = Transaction.objects.filter(amount__lt=0).exclude(category__name='Credit Card Payments')
    original_df = DataFrame(data=[{k: getattr(t, k) for k in ('date', 'category', 'amount')} for t in trx])

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
