from django.views.generic import ListView
from finance.models import Account, Transaction


class InstitutionList(ListView):
    model = Transaction
