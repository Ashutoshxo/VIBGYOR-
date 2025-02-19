from django import forms
from .models import Task, TaskAssignment
from employee.models import Employe_User  

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['task_title', 'task_description', 'task_priority', 'start_date', 'end_date', 'task_type']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

class TaskAssignmentForm(forms.ModelForm):
    class Meta:
        model = TaskAssignment
        fields = ['task', 'assigned_to', 'status']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)  # Get logged-in user
        super().__init__(*args, **kwargs)

        if self.request:
            # Make sure request.user is an instance of Employe_User
            if isinstance(self.request.user, Employe_User):
                # Filter based on reporting_manager
                self.fields['assigned_to'].queryset = Employe_User.objects.filter(reporting_manager=self.request.user)
            else:
                self.fields['assigned_to'].queryset = Employe_User.objects.none()  # If not an Employe_User, show nothing

