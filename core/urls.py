from django.urls import path
from . import views
from .views import admin_panel,admin_users, toggle_user_status

app_name = 'core'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('admin-panel/', admin_panel, name='admin_panel'),
    path('admin-panel/users/',views.admin_users, name='admin_users'),
    path('admin-panel/users/toggle/<int:user_id>/', views.toggle_user_status, name='toggle_user'),
    path('admin-panel/users/promote/<int:user_id>/', views.promote_to_staff, name='promote_user'),
    path( 'admin-panel/users/demote/<int:user_id>/',views.demote_from_staff, name='demote_user'),
    path('admin-panel/targets/', views.admin_targets, name='admin_targets'),
    path('admin-panel/targets/delete/<int:target_id>/',views.admin_delete_target,name='admin_delete_target'),
    path('admin-panel/scans/', views.admin_scans, name='admin_scans'),
    path( 'admin-panel/scans/delete/<int:scan_id>/',   views.admin_delete_scan,  name='admin_delete_scan'),
    path('admin-panel/logs/', views.admin_logs, name='admin_logs'),  # ✅ هذا السطر
    path('staff-panel/', views.staff_panel, name='staff_panel'),


   


]
