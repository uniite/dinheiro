import django.db
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render
from ofxhome import OFXHome

from finance.forms import InstitutionForm
from finance.models import Institution

import api


@login_required
def add(request, id):
    inst = Institution()
    if request.method == "GET":
        if id:
            info = OFXHome.lookup(int(id))
            inst.name = info.name
            inst.fid = info.fid
            inst.org = info.org
            inst.url = info.url
            inst.clean()
            form = InstitutionForm(instance=inst)
        else:
            pass
    elif request.method == "POST":
        form = InstitutionForm(data=request.POST, instance=inst)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse(show, args=(inst.pk,)))
        else:
            request.user.message_set.create(message='Please check your data.')

    return render(request, "institutions/add.html", {"inst_form": form})

@login_required
def index(request):
    return render(request, "institutions/index.html", {"institutions": Institution.objects.all()})

@login_required
def search(request):
     return render(request, "institutions/search.html")

@login_required
def search_results(request):
    if "q" in request.POST:
        results = OFXHome.search(request.POST["q"])
    else:
        results = []
    return render(request, "institutions/search_results.html", {"results": results})

@login_required
def show(request, pk):
    inst = get_object_or_404(Institution, pk=pk)
    accounts = {}
    for acct in inst.account_set.all():
        stmt = acct.statement(days=7)
        accounts[acct.number] = {
                "description": acct.description,
                "statement": stmt
        }
    return render(request, "institutions/show.html", {"inst": inst, "accounts": accounts})
