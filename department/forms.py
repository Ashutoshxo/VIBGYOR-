from django import forms
from .models import Department, Role, User, Task, Leave, Performance
from django.contrib.auth.forms import UserCreationForm


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['dept_name', 'description', 'status']



class RoleForm(forms.ModelForm):
    class Meta:
        model = Role
        fields = ['role_name', 'description']  




class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'department', 'role', 'profile_picture']



class PerformanceForm(forms.ModelForm):
    class Meta:
        model = Performance
        fields = ['review_date', 'feedback', 'goals', 'accomplishments']


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['task_name', 'description', 'due_date', 'completed']


class LeaveForm(forms.ModelForm):
    class Meta:
        model = Leave
        fields = ['leave_type', 'start_date', 'end_date', 'status']


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
