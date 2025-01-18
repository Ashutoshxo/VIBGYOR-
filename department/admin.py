from django.contrib import admin

# Register your models here.

from .models import Department, Role, User, Performance, Task, Leave

class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('dept_name', 'description', 'status')  
    search_fields = ('dept_name',)  
    list_filter = ('status',) 

admin.site.register(Department, DepartmentAdmin)

class RoleAdmin(admin.ModelAdmin):
    list_display = ('role_name', 'description')
    search_fields = ('role_name',)
    
admin.site.register(Role, RoleAdmin)

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email', 'department', 'role', 'is_active')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    list_filter = ('is_active', 'department', 'role')

admin.site.register(User, UserAdmin)

class PerformanceAdmin(admin.ModelAdmin):
    list_display = ('user', 'review_date', 'goals', 'accomplishments')
    search_fields = ('user__username', 'review_date')
    
admin.site.register(Performance, PerformanceAdmin)


class TaskAdmin(admin.ModelAdmin):
    list_display = ('task_name', 'description', 'due_date', 'completed')
    search_fields = ('task_name',)
    list_filter = ('completed',)

admin.site.register(Task, TaskAdmin)

class LeaveAdmin(admin.ModelAdmin):
    list_display = ('leave_type', 'start_date', 'end_date', 'status', 'user')
    search_fields = ('user__username', 'leave_type')
    list_filter = ('status', 'leave_type')

admin.site.register(Leave, LeaveAdmin)
