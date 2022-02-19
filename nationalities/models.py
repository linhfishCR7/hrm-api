from django.db import models
from base.models import BaseModel

# Create your models here.
class Nationalities(BaseModel):
    # Nationalities
    nationality = models.CharField(max_length=255)
    name = models.CharField(max_length=255, default=None)