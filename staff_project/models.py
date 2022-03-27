from django.db import models
from base.models import BaseModel

# Create your models here.
class StaffProject(BaseModel):
    # Staff Project
    project = models.ForeignKey('projects.Projects', on_delete=models.CASCADE, related_name='staff_project_project')
    staff = models.ForeignKey('staffs.Staffs', on_delete=models.CASCADE, related_name='staff_project_staff')