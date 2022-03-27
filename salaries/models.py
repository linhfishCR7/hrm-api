from django.db import models
from base.models import BaseModel

# Create your models here.
class Salary(BaseModel):
    # Salary
    date = models.DateField()
    standard_time = models.IntegerField(default=1, null=True, blank=True)
    actual_time = models.IntegerField(default=1, null=True, blank=True)
    basic_salary = models.IntegerField(null=True, blank=True)
    extra = models.IntegerField(null=True, blank=True)
    coefficient = models.FloatField(null=True, blank=True)
    allowance = models.FloatField(null=True, blank=True)
    other_support = models.IntegerField(null=True, blank=True)
    tax = models.IntegerField(null=True, blank=True)
    overtime = models.IntegerField(null=True, blank=True)
    other = models.IntegerField(null=True, blank=True)
    note = models.CharField(max_length=255, default=None, null=True, blank=True)
    staff = models.ForeignKey('staffs.Staffs', on_delete=models.CASCADE, related_name='salary_staff')