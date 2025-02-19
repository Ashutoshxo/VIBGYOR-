from django.contrib.auth.models import AbstractUser, User
from django.db import models
from role_management.models import Role, UserRole

class Employe_User(AbstractUser):
    # Linking to the User model using OneToOneField
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="employee_user")
    is_manager = models.BooleanField(default=False)
    # Custom fields for the employee model
    employee_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    mobile = models.CharField(max_length=100, unique=True)
    
    # ForeignKey relationships for department and role
    dept = models.ForeignKey('department.Department', on_delete=models.SET_NULL, null=True, related_name="employees")
    role = models.ForeignKey('role_management.Role', on_delete=models.SET_NULL, null=True, related_name="users")
    
    # Reporting Manager relationship (self-referential FK)
    reporting_manager = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True)
    
    # Date of joining, timestamps
    date_of_joining = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Username and password for the user model (Django provides these by default in AbstractUser)
    username = models.CharField(max_length=150, unique=True, blank=False)
    password = models.CharField(max_length=128)  # Django stores hashed passwords

    # User Permissions & Groups
    groups = models.ManyToManyField(
        "auth.Group",
        related_name="custom_user_set",
        blank=True
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="custom_user_set",
        blank=True
    )

    def save(self, *args, **kwargs):
        # Assign the reporting manager if it's not already set
        if not self.reporting_manager:
            try:
                # Get the first UserRole associated with an "HR" role for reporting manager assignment
                user_role = UserRole.objects.filter(role__role_name="HR").first()
                
                # If found, assign their user as the reporting manager
                if user_role:
                    self.reporting_manager = user_role.user
                else:
                    self.reporting_manager = None
            except UserRole.DoesNotExist:
                self.reporting_manager = None

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.username}"

