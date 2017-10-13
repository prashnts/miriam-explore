from django.conf.urls import url
from django.views.generic import TemplateView, RedirectView

from . import views

urlpatterns = [
    url(r'^$', RedirectView.as_view(url='/'), name='browser_home'),
    url(r'^network/$', TemplateView.as_view(template_name='browser/network.html'), name='browser_network'),
    url(r'^heatmap/$', TemplateView.as_view(template_name='browser/heatmap.html'), name='browser_heatmap'),
    url(r'^sankey/$', views.sankey, name='browser_sankey'),
]
