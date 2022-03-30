from django.db import models
from base.models import BaseModel

# Create your models here.
class RecruitmentRequirementDetail(BaseModel):
    # Recruitment Requirement Detail
    time_to_finish = models.DateField()
    content = models.TextField(default=None) 
    position_requirement = models.CharField(max_length=255, default=None) 
    amount = models.IntegerField()
    recuitment_requirement = models.ForeignKey('recruitment_requirements.RecruitmentRequirement', on_delete=models.CASCADE, related_name='recruitment_requirements_detail_recruitment_requirements')