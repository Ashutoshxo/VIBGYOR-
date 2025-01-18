from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Department(models.Model):
    dept_id = models.AutoField(primary_key=True)  
    dept_name = models.CharField(max_length=100)  
    description = models.CharField(max_length=300) 
    created_at = models.DateTimeField(auto_now_add=True)  
    updated_at = models.DateTimeField(auto_now=True)  
    status = models.BooleanField(default=True) 

    def __str__(self):
        return self.dept_name
    
class Role(models.Model):
    role_name = models.CharField(max_length=100) 
    description = models.CharField(max_length=300, blank=True, null=True)

    def __str__(self):
        return self.role_name



from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True)
    profile_picture = models.ImageField(upload_to='user_profile_pics/', blank=True, null=True)
    
    groups = models.ManyToManyField('auth.Group', related_name='department_user_groups', blank=True)
    user_permissions = models.ManyToManyField('auth.Permission', related_name='department_user_permissions', blank=True)

    def __str__(self):
        return self.username


class Performance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    review_date = models.DateField()  
    feedback = models.TextField()  
    goals = models.TextField()  
    accomplishments = models.TextField()  

    def __str__(self):
        return f"Performance Review for {self.user.username} on {self.review_date}"

class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  
    task_name = models.CharField(max_length=255)  
    description = models.TextField()  
    due_date = models.DateTimeField()  
    completed = models.BooleanField(default=False)  

    def __str__(self):
        return f"Task: {self.task_name} for {self.user.username}"


class Leave(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  
    leave_type = models.CharField(max_length=50)  
    start_date = models.DateField() 
    end_date = models.DateField() 
    status = models.CharField(max_length=50, choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')], default='Pending')  # Leave status

    def __str__(self):
        return f"Leave Request for {self.user.username} from {self.start_date} to {self.end_date}"

   