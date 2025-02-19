# Generated by Django 5.1.2 on 2025-02-17 11:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0001_initial'),
        ('task', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='taskassignment',
            name='employee',
        ),
        migrations.AddField(
            model_name='taskassignment',
            name='assigned_to',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='assigned_tasks', to='employee.employe_user'),
        ),
        migrations.AlterField(
            model_name='task',
            name='task_description',
            field=models.TextField(blank=True, max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='task_priority',
            field=models.CharField(choices=[('High', 'High'), ('Medium', 'Medium'), ('Low', 'Low')], default='Medium', max_length=10),
        ),
        migrations.AlterField(
            model_name='task',
            name='task_type',
            field=models.CharField(choices=[('Individual', 'Individual'), ('Team', 'Team')], default='Individual', max_length=10),
        ),
        migrations.AlterField(
            model_name='taskassignment',
            name='assigned_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='tasks_assigned', to='employee.employe_user'),
        ),
        migrations.AlterField(
            model_name='taskassignment',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('In Progress', 'In Progress'), ('Completed', 'Completed')], default='Pending', max_length=15),
        ),
        migrations.AlterField(
            model_name='taskassignment',
            name='task',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assignments', to='task.task'),
        ),
    ]
