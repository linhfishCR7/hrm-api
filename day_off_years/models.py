from django.db import models
from django.utils import timezone
from base.models import BaseModel

# Create your models here.
class DayOffYears(BaseModel):
    # DayOffYears
    date = models.DateField(default=timezone.now())
    reason = models.TextField(default=None, null=True, blank=True)
    contact = models.TextField(default=None, null=True, blank=True)
    status = models.BooleanField(default=False)
    hand_over = models.CharField(max_length=255, null=True, blank=True)
    approved_by = models.ForeignKey(
        'staffs.Staffs', 
        on_delete=models.CASCADE, 
        related_name='approved_by_staff',
        null=True, 
        blank=True
    )
    staff = models.ForeignKey('staffs.Staffs', on_delete=models.CASCADE, related_name='day_off_year_staff')