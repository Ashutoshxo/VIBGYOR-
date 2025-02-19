from django.db import models
from django.contrib.auth.models import User, Permission

from django.db import models

class Role(models.Model):
    role_id = models.AutoField(primary_key=True)  
    role_name = models.CharField(max_length=100)  
    description = models.CharField(max_length=200, blank=True, null=True)  
    created_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now=True)  
    status = models.BooleanField(default=True)  

    def __str__(self):
        return self.role_name


from django.db import models
from django.contrib.auth.models import User
from role_management.models import Role
from django.contrib.auth.models import Permission

class UserRole(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    permissions = models.ManyToManyField(Permission, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.role.role_name}"

