from django.db import models
from base.models import BaseModel

# Create your models here.
class HealthStatus(BaseModel):
    # HealthStatus
    date = models.DateField(default=None)
    content = models.TextField(default=None, null=True, blank=True)
    place = models.CharField(max_length=255, default=None)
    health_status = models.CharField(max_length=255, default=None)
    staff = models.ForeignKey('staffs.Staffs', on_delete=models.CASCADE, related_name='heathy_status_staff')