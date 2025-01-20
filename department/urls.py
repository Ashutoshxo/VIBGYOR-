from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('departments/', views.department_list, name='department_list'),
    path('department/create/', views.department_create, name='department_create'),
    path('department/update/<int:dept_id>/', views.department_update, name='department_update'),
    path('department/delete/<int:dept_id>/', views.department_delete, name='department_delete'),

    path('roles/', views.role_list, name='role_list'),
    path('role/create/', views.role_create, name='role_create'),
    path('role/update/<int:role_id>/', views.role_update, name='role_update'),
    path('role/delete/<int:role_id>/', views.role_delete, name='role_delete'),

  
    path('users/', views.user_list, name='user_list'),
    path('user/create/', views.user_create, name='user_create'),
    path('user/update/<int:user_id>/', views.user_update, name='user_update'),
    path('user/delete/<int:user_id>/', views.user_delete, name='user_delete'),

    path('performance/create/<int:user_id>/', views.performance_create, name='performance_create'),
    path('performance/list/<int:user_id>/', views.performance_list, name='performance_list'),
    path('performance/delete/<int:performance_id>/', views.performance_delete, name='performance_delete'),

    path('task/create/<int:user_id>/', views.task_create, name='task_create'),
    path('task/list/<int:user_id>/', views.task_list, name='task_list'),
    path('task/delete/<int:task_id>/', views.task_delete, name='task_delete'),
    path('task/update/<int:task_id>/', views.task_update, name='task_update'),

    path('leave/create/<int:user_id>/', views.leave_create, name='leave_create'),
    path('leave/list/<int:user_id>/', views.leave_list, name='leave_list'),
    path('leave/delete/<int:leave_id>/', views.leave_delete, name='leave_delete'),

    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', views.custom_logout, name='logout'),
    path('signup/', views.signup, name='signup'),
]
