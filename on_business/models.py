from django.db import models
from base.models import BaseModel

# Create your models here.
class OnBusiness(BaseModel):
    # Skills
    date = models.DateField()
    company = models.CharField(max_length=255, default=None)
    position = models.CharField(max_length=255, default=None)
    content = models.CharField(max_length=255, default=None)
    start_date = models.DateField()
    staff = models.ForeignKey('staffs.Staffs', on_delete=models.CASCADE, related_name='on_business_staff')