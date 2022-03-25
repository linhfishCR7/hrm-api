from django.db import models
from base.models import BaseModel

# Create your models here.
class Degree(BaseModel):
    # Degree
    number = models.CharField(max_length=255, default=None)
    name = models.CharField(max_length=255, default=None)
    date = models.DateField()
    place = models.CharField(max_length=255, default=None)
    attach = models.CharField(max_length=255, default=None)
    type = models.ForeignKey('degree_types.DegreeTypes', on_delete=models.CASCADE, related_name='degree_degree_type')
    staff = models.ForeignKey('staffs.Staffs', on_delete=models.CASCADE, related_name='degree_staff')