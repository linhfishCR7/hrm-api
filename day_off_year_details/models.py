from django.db import models
from django.utils import timezone
from base.models import BaseModel

# Create your models here.
class DayOffYearDetails(BaseModel):
    # DayOffYears
    from_date = models.DateField()
    to_date = models.DateField()
    amount = models.IntegerField(default=1)
    note = models.TextField(default=None, null=True, blank=True)

    day_off_years = models.ForeignKey('day_off_years.DayOffYears', on_delete=models.CASCADE, related_name='day_off_year_day_off_year_detail')
    day_off_types = models.ForeignKey('day_off_types.DayOffTypes', on_delete=models.CASCADE, related_name='day_off_type_day_off_year_detail')