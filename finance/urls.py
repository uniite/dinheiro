from django.conf.urls import patterns, include, url
from rest_framework.routers import DefaultRouter

from finance import views


# Create a router and register our viewsets with it
router = DefaultRouter(trailing_slash=False)
router.register(r'accounts', views.api.AccountViewSet)
router.register(r'categories', views.api.CategoryViewSet)
router.register(r'transactions', views.api.TransactionViewSet)
router.register(r'rules', views.api.CategoryRuleViewSet)
router.register(r'stats', views.api.StatsViewSet, base_name="stats")
router.register(r'summary_stats', views.api.SummaryStatsViewSet, base_name="summary_stats")


urlpatterns = patterns('',
        url(r'^$', 'finance.views.index', name='inst-index'),
        url(r'^api/', include(router.urls)),
        url(r'^institutions/?$', 'finance.views.institutions.list', name='inst-list'),
        url(r'^institutions/add/(\d+)?$', 'finance.views.add', name='inst-add'),
        url(r'^institutions/search/?$', 'finance.views.search', name='inst-search'),
        url(r'^institutions/search_results/?$', 'finance.views.search_results', name='inst-search-results'),
        url(r'^transactions/stats/?$', 'finance.views.transactions.stats', name='transaction-stats'),
)
