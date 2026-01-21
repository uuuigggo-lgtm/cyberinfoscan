from django.urls import path
from . import views

app_name = 'targets'

urlpatterns = [
    path('', views.target_list, name='list'),
    path('add/', views.target_add, name='add'),
    path('edit/<int:pk>/', views.target_edit, name='edit'),
    path('delete/<int:pk>/', views.target_delete, name='delete'),
]
