from django.db import models
from base.models import BaseModel

# Create your models here.
class KindsOfWork(BaseModel):
    # Kind of word
    work = models.CharField(max_length=255)
    name = models.CharField(max_length=255, default=None)
