from django.db import models


# Create your models here.



# class Department(models.Model):
#     dept_id = models.AutoField(primary_key=True)
#     dept_name = models.CharField(max_length=100)
#     description = models.CharField(max_length=300)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     status = models.BooleanField(default=True)
#     is_deleted = models.BooleanField(default=False) 

#     def __str__(self):
#         return self.dept_name

# from django.db import models

class Department(models.Model):
    dept_id = models.AutoField(primary_key=True)
    dept_name = models.CharField(max_length=100)
    description = models.TextField(max_length=300, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True)  # Soft delete implementation

    def __str__(self):
        return self.dept_name



from django.db import models
from employee.models import Employe_User  # Assuming you have an Employee model
from django.utils import timezone

LEAVE_CHOICES = [
    ('SL', 'Sick Leave'),
    ('CL', 'Casual Leave'),
    ('PL', 'Paid Leave'),
    ('LWP', 'Leave Without Pay')
]

STATUS_CHOICES = [
    ('pending', 'Pending'),
    ('approved', 'Approved'),
    ('rejected', 'Rejected')
]

class Leave(models.Model):
    employee = models.ForeignKey(Employe_User, on_delete=models.CASCADE)
    leave_type = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    status = models.CharField(max_length=100, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Leave request by {self.employee.first_name} {self.employee.last_name} ({self.leave_type})"



class LeaveQuota(models.Model):
    employee = models.ForeignKey(Employe_User, on_delete=models.CASCADE)
    leave_type = models.CharField(max_length=3, choices=LEAVE_CHOICES)  # Fixed 'max_length' to 3
    total_quota = models.IntegerField()
    used_quota = models.IntegerField(default=0)
    remain_quota = models.IntegerField()

    class Meta:
        unique_together = ('employee', 'leave_type')  # Enforce unique quota per employee and leave type

    def __str__(self):
        return f"{self.employee.username} - {self.leave_type}"
