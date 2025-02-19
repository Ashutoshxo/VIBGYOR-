from django.shortcuts import render

# Create your views here.
# authentication/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import LoginForm
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User as AuthUser
from django.contrib.auth.forms import SetPasswordForm
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from django.contrib import messages
import random


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                
                
                if user.is_superuser:
                    return redirect('department_dashboard')  
                else:
                    return redirect('index')  
                
            else:
                messages.error(request, 'Invalid credentials')
    else:
        form = LoginForm()

    return render(request, 'authentication/login.html', {'form': form})





def send_otp_email(user_email, otp):
    send_mail(
        'Password Reset OTP',
        f'Your OTP for password reset is {otp}',
        'no-reply@yourdomain.com',
        [user_email],
        fail_silently=False,
    )

def password_reset_request(request):
    if request.method == 'POST':
        email = request.POST['email']
        try:
            user = AuthUser.objects.get(email=email)
            otp = random.randint(100000, 999999)
            request.session['otp'] = otp  # Store OTP in session
            send_otp_email(email, otp)
            messages.success(request, 'OTP sent to your email')
            return redirect('password_reset_otp')
        except AuthUser.DoesNotExist:
            messages.error(request, 'Email not registered')
            return redirect('password_reset_request')

    return render(request, 'authentication/password_reset_request.html')

def password_reset_otp(request):
    if request.method == 'POST':
        otp = request.POST['otp']
        if str(request.session.get('otp')) == otp:
            return redirect('password_reset_new_password')
        else:
            messages.error(request, 'Invalid OTP')
            return redirect('password_reset_otp')

    return render(request, 'authentication/password_reset_otp.html')

def password_reset_new_password(request):
    if request.method == 'POST':
        password = request.POST['password']
        password_confirm = request.POST['password_confirm']
        if password == password_confirm:
            user = AuthUser.objects.get(email=request.session.get('email'))
            user.set_password(password)
            user.save()
            messages.success(request, 'Password updated successfully')
            return redirect('user_login')
        else:
            messages.error(request, 'Passwords do not match')

    return render(request, 'authentication/password_reset_new_password.html')