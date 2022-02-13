from django.db import models
from base.models import BaseModel

# Create your models here.
class DayOffTypes(BaseModel):
    # Day Off Types
    day_off_types = models.CharField(max_length=255)
    name = models.CharField(max_length=255, default=None)