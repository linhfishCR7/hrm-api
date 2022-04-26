from django.db import models
from base.models import BaseModel

# Create your models here.
class EmploymentContract(BaseModel):
    # Employment Contract
    number_contract = models.CharField(max_length=255, default="MTC-HDLD-0000")
    name = models.CharField(max_length=255)
    from_date = models.DateField()
    to_date = models.DateField()
    place_working = models.CharField(max_length=255, default=None, null=True, blank=True)
    number_employee = models.CharField(max_length=255, default="N/A", null=True, blank=True)
    content = models.TextField(default="Theo sự phân công của giám đốc", null=True, blank=True)
    time_working = models.CharField(max_length=255, default="Theo nội qui của công ty", null=True, blank=True)
    uniform = models.CharField(max_length=255, default="Theo nội qui của công ty", null=True, blank=True)
    vehicles = models.CharField(max_length=255, default="Tự túc", null=True, blank=True)
    basic_salary = models.IntegerField(null=True, blank=True)
    extra = models.IntegerField(null=True, blank=True)
    other_support = models.IntegerField(null=True, blank=True)
    transfer = models.CharField(max_length=255, default="Chuyển khoản ngân hàng", null=True, blank=True)
    up_salary = models.CharField(max_length=255, default="Theo qui định của công ty", null=True, blank=True)
    bonus = models.CharField(max_length=255, default="Theo qui định của công ty", null=True, blank=True)
    training = models.CharField(max_length=255, default="Theo qui định của công ty", null=True, blank=True)
    resort_mode = models.CharField(max_length=255, default="Theo qui định của công ty", null=True, blank=True)
    insurance = models.CharField(max_length=255, default="Theo qui định của công ty", null=True, blank=True)
    sign_day = models.DateField()
    status = models.BooleanField(default=False)
    employer = models.CharField(max_length=255, default="Huỳnh Tuấn Hoàng")
    position = models.CharField(max_length=255, default="Giám đốc")
    type = models.ForeignKey('employment_contract_types.EmploymentContractTypes', on_delete=models.CASCADE, related_name='employment_contract_employment_contract_types')
    staff = models.ForeignKey('staffs.Staffs', on_delete=models.CASCADE, related_name='employment_contract_staff')