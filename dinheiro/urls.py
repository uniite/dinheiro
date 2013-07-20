from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'dinheiro.views.home', name='home'),
    # url(r'^dinheiro/', include('dinheiro.foo.urls')),
	url(r'^$', 'finance.views.index'),
	url(r'^finance/?$', 'finance.views.index', name='inst-index'),
	url(r'^finance/(\d+)?$', 'finance.views.show', name='inst-show'),
	url(r'^finance/add/(\d+)?$', 'finance.views.add', name='inst-add'),
	url(r'^finance/search/?$', 'finance.views.search', name='inst-search'),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
