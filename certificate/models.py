from django.db import models
from base.models import BaseModel

# Create your models here.
class Certificate(BaseModel):
    # Certificate
    number = models.CharField(max_length=255, default=None)
    name = models.CharField(max_length=255, default=None)
    level = models.CharField(max_length=255, default=None)
    date = models.DateField()
    expire = models.DateField()
    place = models.CharField(max_length=255, default=None)
    note = models.TextField(max_length=255, default=None)
    attach = models.CharField(max_length=255, default=None)
    type = models.ForeignKey('certificate_types.CertificateTypes', on_delete=models.CASCADE, related_name='certificate_certificate_type')
    staff = models.ForeignKey('staffs.Staffs', on_delete=models.CASCADE, related_name='certificate_staff')