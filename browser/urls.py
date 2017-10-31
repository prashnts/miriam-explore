from django.urls import path
from django.views.generic import TemplateView, RedirectView

from . import views

urlpatterns = [
    path('/', RedirectView.as_view(url='/'), name='browser_home'),
    path('network/', TemplateView.as_view(template_name='browser/network.html'), name='browser_network'),
    path('heatmap/', TemplateView.as_view(template_name='browser/heatmap.html'), name='browser_heatmap'),
    path('sankey/', views.sankey, name='browser_sankey'),

    path('tables/', views.tables, name='browser_tables'),
    path('tables/<str:sample_id>/', views.tables, name='browser_tables'),
    path('tables/<str:sample_id>/<int:page>/', views.tables, name='browser_tables'),
    path('tables/<str:sample_id>/download/', views.tables_download, name='browser_table_download'),
]
