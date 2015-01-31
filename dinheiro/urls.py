from django.conf.urls import patterns, include, url
from django.contrib import admin

from dinheiro import settings
from dinheiro.views import HomeView
from finance.views.transactions import TransactionListView


admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'dinheiro.views.home', name='home'),
    # url(r'^dinheiro/', include('dinheiro.foo.urls')),
    url(r'^$', HomeView.as_view()),

    url(r'^finance/', include('finance.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

# if settings.DEBUG:
#     urlpatterns += patterns('',
#         (r'^%s/(?P<path>.*)$' % settings, 'django.views.static.serve',
#         {'document_root': settings.STATIC_ROOT, 'show_indexes': True})
#     )

