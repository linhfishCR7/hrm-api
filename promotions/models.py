from django.db import models
from base.models import BaseModel

# Create your models here.
class Promotions(BaseModel):
    # Promotions
    date = models.DateField(default=None)
    file = models.CharField(max_length=255, default=None)
    content = models.TextField(default=None, null=True, blank=True)
    note = models.TextField(default=None, null=True, blank=True)
    staff = models.ForeignKey('staffs.Staffs', on_delete=models.CASCADE, related_name='promotion_staff')
    position = models.ForeignKey('positions.Positions', on_delete=models.CASCADE, related_name='promotion_position')

    