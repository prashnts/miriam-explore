from django.conf.urls import url
from django.views.generic import TemplateView


urlpatterns = [
    url(r'^$',
        TemplateView.as_view(template_name='browser/index.html'),
        name='browser/index.html'),
]
