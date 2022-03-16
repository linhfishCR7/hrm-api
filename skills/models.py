from django.db import models
from base.constants.common import SkillTypes
from base.models import BaseModel

# Create your models here.
class Skills(BaseModel):
    # Skills
    name = models.CharField(max_length=255, default=None)
    type = models.CharField(max_length=255, default=SkillTypes.OFFICE)
    staff = models.ForeignKey('staffs.Staffs', on_delete=models.CASCADE, related_name='skill_staff')