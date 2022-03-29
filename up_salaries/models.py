from django.db import models
from base.models import BaseModel

# Create your models here.
class UpSalary(BaseModel):
    # UpSalary
    date = models.DateField()
    old_coefficient = models.FloatField(default=1.2)
    coefficient = models.FloatField()
    staff = models.ForeignKey('staffs.Staffs', on_delete=models.CASCADE, related_name='up_salary_staff')