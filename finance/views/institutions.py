from django.views.generic import ListView, DetailView
from finance.models import Institution


class InstitutionList(ListView):
    model = Institution
list = InstitutionList.as_view()

class InstitutionDetail(DetailView):
    model = Institution
detail = InstitutionList.as_view()
