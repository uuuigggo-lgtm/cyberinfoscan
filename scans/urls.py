from django.urls import path
from . import views

app_name = 'scans'

urlpatterns = [
    path('', views.scan_list, name='list'),
    path('add/', views.scan_add, name='add'),
    path('delete/<int:pk>/', views.scan_delete, name='delete'),
    path('export/<int:pk>/', views.export_result, name='export'),
]
