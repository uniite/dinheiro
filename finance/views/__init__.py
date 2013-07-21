from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from ofxhome import OFXHome


from finance.serializers import AccountSerializer, InstitutionSerializer, TransactionSerializer
from finance.models import Account, Institution, Transaction
from rest_framework import generics, viewsets
from rest_framework.fields import SerializerMethodField





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


def add(request, id):
	inst = Institution()
	if request.method == "GET":
		if id:
			info = OFXHome.lookup(id)
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

def index(request):
	return render(request, "institutions/index.html", {"institutions": Institution.objects.all()})

def search(request):
	if "q" in request.GET:
		results = OFXHome.search(request.GET["q"])
	else:
		results = []
	return render(request, "institutions/search.html", {"results": results})

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
