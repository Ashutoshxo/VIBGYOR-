from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Department
from .forms import DepartmentForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


def index(request):
    return render(request, 'index.html')

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages

# User Registration View
def register(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        # Check if passwords match
        if password == confirm_password:
            # Check if username or email already exists
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already exists!")
            elif User.objects.filter(email=email).exists():
                messages.error(request, "Email already registered!")
            else:
                # Create a new user
                user = User.objects.create_user(username=username, email=email, password=password)
                user.is_active = True  # Ensure user is active upon registration
                user.save()
                messages.success(request, "Registration successful! You can now login.")
                return redirect('login')
        else:
            messages.error(request, "Passwords do not match!")

    return render(request, 'register.html')

# User Login View
def user_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        # Authenticate user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.is_active:  # Ensure the user is active
                login(request, user)  # Log the user in
                messages.success(request, "Login successful!")

                # Check if the user is staff (admin)
                if user.is_staff:
                    return redirect('department_dashboard')  # Redirect to admin dashboard
                else:
                    messages.warning(request, "No role assigned. Please contact the admin.")
                    return redirect('no_role_page')  # Redirect if no role assigned

            else:
                messages.error(request, "Your account is inactive.")
        else:
            messages.error(request, "Invalid username or password!")

    return render(request, 'login.html')

# User Logout View
def user_logout(request):
    logout(request)  # Log the user out
    return redirect('index')  # Redirect to the index page or home page



def department_dashboard(request):
    if not request.user.is_staff:
        messages.error(request, "Access denied!")
        return redirect('index')
    departments = Department.objects.filter(status=True)
    return render(request, 'dashboard.html', {'departments': departments})

def add_department(request):
    if not request.user.is_staff:
        messages.error(request, "Access denied!")
        return redirect('index')  

    if request.method == "POST":
        form = DepartmentForm(request.POST)
        if form.is_valid():
            form.save()  
            messages.success(request, "Department added successfully!")
            return redirect('department_dashboard')
    else:
        form = DepartmentForm()

    return render(request, 'add_department.html', {'form': form})

def update_department(request, dept_id):
    if not request.user.is_staff:
        messages.error(request, "Access denied!")
        return redirect('index')

    department = get_object_or_404(Department, dept_id=dept_id)
    if request.method == "POST":
        form = DepartmentForm(request.POST, instance=department)
        if form.is_valid():
            form.save()
            messages.success(request, "Department updated successfully!")
            return redirect('department_dashboard')

    else:
        form = DepartmentForm(instance=department)

    return render(request, 'update_department.html', {'form': form, 'department': department})


def delete_department(request, dept_id):
    if not request.user.is_staff:
        messages.error(request, "Access denied!")
        return redirect('index')

    department = get_object_or_404(Department, dept_id=dept_id)

    if request.method == "POST":
        department.status = False  # Soft delete
        department.save()
        messages.success(request, "Department deactivated successfully!")
        return redirect('department_dashboard')

    return render(request, 'confirm_delete.html', {'department': department})





def user_dashboard(request):
    # Your logic here
    return render(request, 'dashboard.html')  # or your actual template

def no_role(request):
    return render(request, 'no_role.html', {'message': "No role assigned. Please contact the admin."})