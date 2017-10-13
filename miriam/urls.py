from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.views.generic import TemplateView, RedirectView
from django.views.defaults import (page_not_found, server_error,
        bad_request, permission_denied)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('landing.urls')),
    url(r'^browser/', include('browser.urls')),

    url(r'^favicon.ico$', RedirectView.as_view(url='/static/img/favicon/favicon.ico', permanent=True)),
    url(r'^privacy-policy/$',
        TemplateView.as_view(template_name='privacy_policy.html'),
        name='privacy_policy'),
    url(r'^contact/$',
        TemplateView.as_view(template_name='contact_us.html'),
        name='contact_us'),
]

if settings.DEBUG:
    urlpatterns += [
        url(r'^400/$', bad_request, kwargs=dict(exception={})),
        url(r'^403/$', permission_denied, kwargs=dict(exception={})),
        url(r'^404/$', page_not_found, kwargs=dict(exception={})),
        url(r'^500/$', server_error),
    ]
