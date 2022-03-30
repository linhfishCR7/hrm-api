from django.db import models
from base.models import BaseModel

# Create your models here.
class TrainningRequirementDetail(BaseModel):
    # Trainning Requirement Detail
    date = models.DateField(null=True, blank=True)
    amount = models.IntegerField()
    note = models.TextField(default=None, null=True, blank=True) 
    staff = models.ForeignKey('staffs.Staffs', on_delete=models.CASCADE, related_name='trainning_requirement_detail_staff')    
    trainning_requirement = models.ForeignKey('trainning_requirement.TrainningRequirement', on_delete=models.CASCADE, related_name='trainning_requirement_detail_trainning_requirement')