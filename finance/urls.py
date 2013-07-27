from django.conf.urls import patterns, include, url
from django.views.generic.base import TemplateView

from finance import views
from finance.views.transactions import TransactionListView

from rest_framework.routers import DefaultRouter

# Create a router and register our viewsets with it
router = DefaultRouter(trailing_slash=False)
router.register(r'accounts', views.api.AccountViewSet)
router.register(r'transactions', views.api.TransactionViewSet)
router.register(r'stats', views.api.StatsViewSet, base_name="stats")

class AccountsView(TemplateView):
    template_name = "finance/accounts.html"


urlpatterns = patterns('',
        url(r'^accounts/?$', AccountsView.as_view(), name='accounts'),
        url(r'^api/', include(router.urls)),
        url(r'^$', 'finance.views.index', name='inst-index'),
        url(r'^institutions/?$', 'finance.views.institutions.list', name='inst-list'),
        url(r'^institutions/(\d+)/?$', 'finance.views.show', name='inst-show'),
        url(r'^institutions/add/(\d+)?$', 'finance.views.add', name='inst-add'),
        url(r'^institutions/search/?$', 'finance.views.search', name='inst-search'),
        url(r'^transactions/?$', TransactionListView.as_view(), name='transactions-list'),
)
