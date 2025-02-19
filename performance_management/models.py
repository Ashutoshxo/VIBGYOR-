from django.db import models
from employee.models import Employe_User

REVIEW_PERIOD_CHOICES = [
    ('Monthly', 'Monthly'),
    ('Quarterly', 'Quarterly'),
    ('Annual', 'Annual'),
]

RATING_CHOICES = [
    (1, '1'),
    (2, '2'),
    (3, '3'),
    (4, '4'),
    (5, '5'),
    (6, '6'),
    (7, '7'),
    (8, '8'),
    (9, '9'),
    (10, '10'),
]

class PerformanceReview(models.Model):
    review_id = models.AutoField(primary_key=True)
    review_title = models.CharField(max_length=100)
    review_date = models.DateField()
    employee = models.ForeignKey(Employe_User, on_delete=models.CASCADE)
    reviewed_by = models.ForeignKey(Employe_User, on_delete=models.CASCADE, related_name='reviewed_by')
    review_period = models.CharField(max_length=100, choices=REVIEW_PERIOD_CHOICES)
    rating = models.IntegerField(choices=RATING_CHOICES)
    comments = models.CharField(max_length=300, blank=True, null=True)
    created_by = models.DateTimeField(auto_now_add=True)
    updated_by = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True)  # Add the status field

    def __str__(self):
        return f"{self.review_title} for {self.employee.first_name} {self.employee.last_name}"
