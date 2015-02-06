from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from finance.models import Institution


class InstitutionList(ListView):
    model = Institution
list = login_required(InstitutionList.as_view())
