from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Department
from .forms import DepartmentForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required





def index(request):
    return render(request, 'index.html')



def register(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already exists!")
            elif User.objects.filter(email=email).exists():
                messages.error(request, "Email already registered!")
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.is_active = True  
                user.save()
                messages.success(request, "Registration successful! You can now login.")
                return redirect('login')
        else:
            messages.error(request, "Passwords do not match!")

    return render(request, 'register.html')


def user_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.is_active:  
                login(request, user)  
                messages.success(request, "Login successful!")

                
                if user.is_staff:
                    return redirect('department_dashboard') 
                else:
                    messages.warning(request, "No role assigned. Please contact the admin.")
                    return redirect('no_role_page')  

            else:
                messages.error(request, "Your account is inactive.")
        else:
            messages.error(request, "Invalid username or password!")

    return render(request, 'login.html')

def user_logout(request):
    logout(request)  
    return redirect('index')  



from django.shortcuts import render, redirect
from django.db import models
from django.contrib import messages
from task.models import TaskAssignment
from department.models import Department

def department_dashboard(request):
    # Check if user is staff (admin or similar role)
    if not request.user.is_staff:
        messages.error(request, "Access denied!")
        return redirect('index')

  
    departments = Department.objects.filter(status=True)

 
    task_counts = TaskAssignment.objects.values('status').annotate(count=models.Count('status'))

  
    task_statuses = {status['status']: status['count'] for status in task_counts}

   
    return render(request, 'dashboard.html', {
        'departments': departments,
        'task_statuses': task_statuses,
    })


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
        department.status = False 
        department.save()
        messages.success(request, "Department deactivated successfully!")
        return redirect('department_dashboard')

    return render(request, 'confirm_delete.html', {'department': department})






def no_role(request):
    return render(request, 'no_role.html', {'message': "No role assigned. Please contact the admin."})


##************************************************************************************************************

from django.shortcuts import render
from .models import Leave, LeaveQuota
from role_management.models import Role  
from employee.models import Employe_User
from django.contrib.auth.decorators import login_required



from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from department.models import LeaveQuota
from employee.models import Employe_User  # Import your custom user model

@login_required
def employee_dashboard(request):
    try:
        # Query the Employe_User model using request.user, which represents the logged-in user
        employee = Employe_User.objects.get(username=request.user.username)  # Querying using the username
    except Employe_User.DoesNotExist:
        employee = None

    # Fetch the leave quotas related to the found employee
    if employee:
        leave_quotas = LeaveQuota.objects.filter(employee=employee)
    else:
        leave_quotas = []

    return render(request, 'employee_dashboard.html', {'leave_quotas': leave_quotas})

# department/views.py

from django.shortcuts import render, redirect
from .forms import LeaveForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import LeaveForm
from django.contrib.auth.decorators import login_required
from employee.models import Employe_User  # Import your custom user model

@login_required
def apply_leave(request):
    if request.method == 'POST':
        form = LeaveForm(request.POST)
        if form.is_valid():
            leave = form.save(commit=False)

            # Fetch the corresponding Employe_User instance
            try:
                employee = Employe_User.objects.get(user=request.user)  # Fetch the Employe_User linked to the current user
            except Employe_User.DoesNotExist:
                return render(request, 'error.html', {'message': 'Employee profile not found.'})

            leave.employee = employee  # Set the employee who is applying for leave (using Employe_User)
            leave.status = 'pending'  # Status is 'pending' by default
            leave.save()

            return redirect('employee_dashboard')  # Redirect back to the dashboard
    else:
        form = LeaveForm()

    return render(request, 'apply_leave.html', {'form': form})


# department/views.py

from django.shortcuts import get_object_or_404, redirect
from .models import Leave
from .forms import LeaveStatusForm
from django.contrib.auth.decorators import login_required

@login_required
def update_leave_status(request, leave_id):
    leave = get_object_or_404(Leave, id=leave_id)

    # Ensure the user is a manager (check if the related Employee_User has is_manager)
    if request.user.employee_user.is_manager:  # Using the employee_user relation
        if request.method == 'POST':
            form = LeaveStatusForm(request.POST)
            if form.is_valid():
                leave.status = form.cleaned_data['status']
                leave.approved_by = request.user  # Mark the manager who approved/rejected
                leave.save()
                return redirect('admin_dashboard')  # Redirect back to the admin dashboard
        else:
            form = LeaveStatusForm(initial={'status': leave.status})

    else:
        return redirect('employee_dashboard')  # Redirect if not a manager

    return render(request, 'department/update_leave_status.html', {'leave': leave, 'form': form})

# department/views.py

from django.shortcuts import get_object_or_404, redirect
from .models import Leave
from django.contrib.auth.decorators import login_required

@login_required
def delete_leave(request, leave_id):
    leave = get_object_or_404(Leave, id=leave_id)

    # Only HR or Admin can delete the leave
    if request.user.is_staff or request.user.is_admin:  
        leave.delete()
        return redirect('admin_dashboard')  # Redirect back to admin dashboard
    else:
        return redirect('employee_dashboard')  # Redirect back to employee dashboard if not authorized

from django.http import HttpResponseForbidden

@login_required
def admin_dashboard(request):
    # Ensure only admin or staff can access the dashboard
    if not request.user.is_staff:
        return HttpResponseForbidden("You do not have permission to view this page.")

    # Fetch pending leave requests. Adjust the filter based on your status choices.
    leaves = Leave.objects.filter(status='Pending')  # Assuming 'Pending' is the status for pending requests
    return render(request, 'admin_dashboard.html', {'leaves': leaves})