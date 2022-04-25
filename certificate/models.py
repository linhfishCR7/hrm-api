from django.db import models
from base.models import BaseModel

# Create your models here.
class Certificate(BaseModel):
    # Certificate
    number = models.CharField(max_length=255, default=None , null=True)
    name = models.CharField(max_length=255, default=None, null=True)
    level = models.CharField(max_length=255, default=None, null=True)
    date = models.DateField()
    expire = models.DateField(null=True)
    place = models.CharField(max_length=255, default=None, null=True)
    note = models.TextField(max_length=255, default=None, null=True)
    attach = models.CharField(max_length=255, default=None, null=True)
    type = models.ForeignKey('certificate_types.CertificateTypes', on_delete=models.CASCADE, related_name='certificate_certificate_type')
    staff = models.ForeignKey('staffs.Staffs', on_delete=models.CASCADE, related_name='certificate_staff')