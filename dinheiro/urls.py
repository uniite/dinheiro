from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'dinheiro.views.home', name='home'),
    # url(r'^dinheiro/', include('dinheiro.foo.urls')),
	url(r'^$', 'institutions.views.index'),
	url(r'^institutions/?$', 'institutions.views.index', name='inst-index'),
	url(r'^institutions/(\d+)?$', 'institutions.views.show', name='inst-show'),
	url(r'^institutions/add/(\d+)?$', 'institutions.views.add', name='inst-add'),
	url(r'^institutions/search/?$', 'institutions.views.search', name='inst-search'),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
