from django.db import models
from django.utils import timezone
from base.constants.common import TypeTimeKeeping
from base.models import BaseModel

# Create your models here.
class Timekeeping(BaseModel):
    # Timekeeping
    date = models.DateField()
    amount_in_project = models.FloatField(default=1, null=True, blank=True)
    amount_time = models.FloatField(default=0, null=True, blank=True)
    note = models.TextField(default=None, null=True, blank=True)
    type = models.FloatField(default=TypeTimeKeeping.ADMININISTRATION)

    type_work = models.ForeignKey('kinds_of_work.KindsOfWork', on_delete=models.CASCADE, related_name='timekeeping_work')
    staff_project = models.ForeignKey('staff_project.StaffProject', on_delete=models.CASCADE, related_name='timekeeping_staff_project', default=None)