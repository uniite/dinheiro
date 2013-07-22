from django.views.generic import ListView

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
