from django.urls import path
from . import views

urlpatterns = [
    path('',views.index, name='index'),
    path('Department', views.department_dashboard, name='department_dashboard'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    
    path('add/', views.add_department, name='add_department'),
    path('update/<int:dept_id>/', views.update_department, name='update_department'),
    path('delete/<int:dept_id>/', views.delete_department, name='delete_department'),
    path('no_role/', views.no_role, name='no_role_page'), 


    path('employee_dashboard/', views.employee_dashboard, name='employee_dashboard'),
    path('apply_leave/', views.apply_leave, name='apply_leave'),
    path('update_leave_status/<int:leave_id>/', views.update_leave_status, name='update_leave_status'),
    path('delete_leave/<int:leave_id>/', views.delete_leave, name='delete_leave'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
]

  
