from django import forms
from .models import PerformanceReview
from employee.models import Employe_User

class PerformanceReviewForm(forms.ModelForm):
    class Meta:
        model = PerformanceReview
        fields = ['employee', 'review_title', 'review_date', 'review_period', 'rating', 'comments']
        widgets = {
            'review_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Extract user from kwargs
        super().__init__(*args, **kwargs)

        if user:
            # Print statement to confirm the user passed into the form
            print("Logged-in user (reporting_manager):", user)

            # Get the associated Employe_User instance
            try:
                employee_user = Employe_User.objects.get(username=user.username)
                # Filter employees by the logged-in user's reporting manager
                employees = Employe_User.objects.filter(reporting_manager=employee_user)
                
                # Debugging: Print out the filtered employees
                print("Filtered Employees:", employees)

                # If employees are found, assign them to the dropdown, otherwise, inform that no employees exist
                if employees.exists():
                    self.fields['employee'].queryset = employees
                else:
                    print("No employees found for this reporting manager.")
            except Employe_User.DoesNotExist:
                print("Employee not found for the logged-in user.")

        else:
            print("No user passed to the form.")

        # Ensure that all form fields have the 'form-control' class
        for field_name, field in self.fields.items():
            field.widget.attrs.setdefault('class', 'form-control')
