from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from .forms import DepartmentForm, RoleForm, UserForm, PerformanceForm, TaskForm, LeaveForm
from .models import Department
from .models import Role

from django.shortcuts import render, redirect, get_object_or_404
from .models import Performance, User, Leave,  Task
from django.shortcuts import render, redirect
from .forms import SignUpForm
from django.shortcuts import render, redirect
from .forms import DepartmentForm
# Create your views here.


def home(request):
    user = request.user  
    return render(request, 'home.html', {'user': user})



def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to login page after successful signup
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})




def department_create(request):
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            form.save() 
            return redirect('department_list')  
    else:
        form = DepartmentForm()
    return render(request, 'department_form.html', {'form': form})


from django.shortcuts import render
from .models import Department

def department_list(request):
    departments = Department.objects.all()  
    return render(request, 'department_list.html', {'departments': departments})





def department_update(request, dept_id):
    department = get_object_or_404(Department, dept_id=dept_id) 
    if request.method == 'POST':
        form = DepartmentForm(request.POST, instance=department)  
        if form.is_valid():
            form.save() 
            return redirect('department_list')
    else:
        form = DepartmentForm(instance=department)
    return render(request, 'department_form.html', {'form': form})



from django.shortcuts import get_object_or_404, redirect
from .models import Department

def department_delete(request, dept_id):
    department = get_object_or_404(Department, dept_id=dept_id)
    department.delete()  
    return redirect('department_list')   







def role_list(request):
    roles = Role.objects.all()
    return render(request, 'role_list.html', {'roles': roles})

def role_create(request):
    if request.method == 'POST':
        form = RoleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('role_list')
    else:
        form = RoleForm()
    return render(request, 'role_form.html', {'form': form})#

def role_update(request, role_id):
    role = get_object_or_404(Role, id=role_id)
    if request.method == 'POST':
        form = RoleForm(request.POST, instance=role)
        if form.is_valid():
            form.save()
            return redirect('role_list')
    else:
        form = RoleForm(instance=role)
    return render(request, 'role_form.html', {'form': form})


def role_delete(request, role_id):
    role = get_object_or_404(Role, id=role_id)
    role.delete()
    return redirect('role_list')







def user_list(request):
    users = User.objects.all()
    return render(request, 'user_list.html', {'users': users})

def user_create(request):
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('user_list')
    else:
        form = UserForm()
    return render(request, 'user_form.html', {'form': form})


def user_update(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user_list')
    else:
        form = UserForm(instance=user)
    return render(request, 'user_form.html', {'form': form})


def user_delete(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    return redirect('user_list')






def performance_create(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = PerformanceForm(request.POST)
        if form.is_valid():
            performance = form.save(commit=False)
            performance.user = user
            performance.save()
            return redirect('performance_list', user_id=user.id)
    else:
        form = PerformanceForm()
    return render(request, 'pro.html', {'form': form, 'user': user})



def performance_list(request, user_id):

    user = get_object_or_404(User, id=user_id)
    performances = Performance.objects.filter(user=user)
    return render(request, 'performance_list.html', {'performances': performances, 'user': user})






def task_create(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = user
            task.save()
            return redirect('task_list', user_id=user.id)
    else:
        form = TaskForm()
    return render(request, 'task_form.html', {'form': form, 'user': user})

def task_list(request, user_id):
    user = get_object_or_404(User, id=user_id)
    tasks = Task.objects.filter(user=user)
    return render(request, 'task_list.html', {'tasks': tasks, 'user': user})






def leave_create(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = LeaveForm(request.POST)
        if form.is_valid():
            leave = form.save(commit=False)
            leave.user = user
            leave.save()
            return redirect('leave_list', user_id=user.id)
    else:
        form = LeaveForm()
    return render(request, 'leave_form.html', {'form': form, 'user': user})


def leave_list(request, user_id):
    user = get_object_or_404(User, id=user_id)
    leaves = Leave.objects.filter(user=user)
    return render(request, 'leave_list.html', {'leaves': leaves, 'user': user})
