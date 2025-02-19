from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.user_login, name='user_login'),
    path('password-reset/', views.password_reset_request, name='password_reset_request'),
    path('password-reset-otp/', views.password_reset_otp, name='password_reset_otp'),
    path('password-reset-new-password/', views.password_reset_new_password, name='password_reset_new_password'),
]