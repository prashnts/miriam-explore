from django.conf.urls import url
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='browser/index.html'), name='browser_home'),
    url(r'^network/$', TemplateView.as_view(template_name='browser/network.html'), name='browser_network'),
    url(r'^heatmap/$', TemplateView.as_view(template_name='browser/heatmap.html'), name='browser_heatmap'),
    url(r'^sankey/$', views.sankey, name='browser_sankey'),
]
