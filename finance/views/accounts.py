from django.views.generic import ListView, DetailView
from finance.models import Account


class AccountList(ListView):
    model = Account
list = AccountList.as_view()

class InstitutionDetail(DetailView):
    model = Account
detail = AccountList.as_view()
