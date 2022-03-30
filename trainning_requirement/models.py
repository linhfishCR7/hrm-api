from django.db import models
from base.models import BaseModel

# Create your models here.
class TrainningRequirement(BaseModel):
    # Trainning Requirement
    date_requirement = models.DateField(null=True, blank=True)
    content = models.TextField(default=None, null=True, blank=True)
    course_name = models.CharField(max_length=255, default=None, null=True, blank=True) 
    organizational_units = models.CharField(max_length=255, default=None, null=True, blank=True) 
    time_organizational = models.DateField(null=True, blank=True)
    estimated_cost = models.FloatField()
    place = models.CharField(max_length=255, default=None, null=True, blank=True)
    sign_by = models.CharField(max_length=255, default=None, null=True, blank=True)
    unit_head = models.CharField(max_length=255, default=None, null=True, blank=True)
    approved_by = models.CharField(max_length=255, default=None, null=True, blank=True)
    unit = models.CharField(max_length=255, default=None, null=True, blank=True)
    branch = models.ForeignKey('branchs.Branchs', on_delete=models.CASCADE, related_name='trainning_requirements_branch')