from django.db import models
from base.models import BaseModel

# Create your models here.
class Bonuses(BaseModel):
    # Bonuses
    date = models.DateField(default=None)
    amount = models.FloatField(default=0.0)
    reason = models.CharField(max_length=255, default=None)
    note = models.TextField(default=None, null=True, blank=True)
    staff = models.ForeignKey('staffs.Staffs', on_delete=models.CASCADE, related_name='bonus_staff')