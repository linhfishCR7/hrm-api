from django.db import models
from base.models import BaseModel

# Create your models here.
class Discipline(BaseModel):
    # Discipline
    content = models.TextField(default=None)
    date = models.DateField()
    expire = models.DateField()
    attach = models.CharField(max_length=255, default=None)
    note = models.CharField(max_length=255, default=None)
    form_of_discipline = models.CharField(max_length=255, default=None)
    staff = models.ForeignKey('staffs.Staffs', on_delete=models.CASCADE, related_name='discipline_staff')