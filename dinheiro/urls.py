from functools import wraps
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.staticfiles.views import serve as serve_static

from dinheiro import settings


admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'dinheiro.views.home'),
    url(r'^accounts/', include('accounts.urls')),
    url(r'^finance/', include('finance.urls')),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)


# Bust caching on iOS
if settings.DEBUG:

    def custom_headers(view_func):

        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            response = view_func(request, *args, **kwargs)
            response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
            response['Expires'] = '0'
            return response

        return wrapper

    urlpatterns += patterns('',
        url(r'^static/(?P<path>.*)$', custom_headers(serve_static)),
    )
