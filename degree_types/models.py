from django.db import models
from base.models import BaseModel

# Create your models here.
class DegreeTypes(BaseModel):
    # DegreeTypes
    degree_types = models.CharField(max_length=255)
    name = models.CharField(max_length=255, default=None)