from django.db import models
from base.models import BaseModel

# Create your models here.
class EmploymentContract(BaseModel):
    # Employment Contract
    number_contract = models.CharField(max_length=255, default="MTC-HDLD-0000")
    name = models.CharField(max_length=255)
    from_date = models.DateField()
    to_date = models.DateField()
    place_working = models.CharField(max_length=255, default=None)
    number_employee = models.CharField(max_length=255, default="N/A")
    content = models.TextField(default="Theo sự phân công của giám đốc", null=True, blank=True)
    time_working = models.CharField(max_length=255, default="Theo nội qui của công ty")
    uniform = models.CharField(max_length=255, default="Theo nội qui của công ty")
    vehicles = models.CharField(max_length=255, default="Tự túc")
    basic_salary = models.IntegerField(null=True, blank=True)
    extra = models.IntegerField(null=True, blank=True)
    other_support = models.IntegerField(null=True, blank=True)
    transfer = models.CharField(max_length=255, default="Chuyển khoản ngân hàng")
    up_salary = models.CharField(max_length=255, default="Theo qui định của công ty")
    bonus = models.CharField(max_length=255, default="Theo qui định của công ty")
    training = models.CharField(max_length=255, default="Theo qui định của công ty")
    resort_mode = models.CharField(max_length=255, default="Theo qui định của công ty")
    insurance = models.CharField(max_length=255, default="Theo qui định của công ty")
    sign_day = models.DateField()
    status = models.BooleanField(default=False)
    employer = models.CharField(max_length=255, default="Huỳnh Tuấn Hoàng")
    position = models.CharField(max_length=255, default="Giám đốc")
    type = models.ForeignKey('employment_contract_types.EmploymentContractTypes', on_delete=models.CASCADE, related_name='employment_contract_employment_contract_types')
    staff = models.ForeignKey('staffs.Staffs', on_delete=models.CASCADE, related_name='employment_contract_staff')