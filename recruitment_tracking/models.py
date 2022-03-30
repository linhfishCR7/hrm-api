from django.db import models
from base.models import BaseModel

# Create your models here.
class RecruitmentTracking(BaseModel):
    # Recruitment Tracking
    position_recruiment = models.CharField(max_length=255, null=True, blank=True)
    date_receive_receipt_of_application = models.DateField()
    is_job_application = models.BooleanField(default=False)
    is_cv = models.BooleanField(default=False)
    is_diploma = models.BooleanField(default=False)
    is_health_certification = models.BooleanField(default=False)
    office_day01 = models.DateField()
    is_qualification01 = models.BooleanField(default=False)
    office_day02 = models.DateField()
    is_qualification02 = models.BooleanField(default=False)
    is_agree_recruiment = models.BooleanField(default=False)
    contact_before_sign_contract = models.CharField(max_length=255, default=None)
    date_start_work = models.DateField()
    salary_start = models.FloatField()
    is_receive_recruing_decision = models.BooleanField(default=False)
    date_receive_recruing_decision = models.DateField()
    recruitment_requirement_details = models.ForeignKey('recruitment_requirement_details.RecruitmentRequirementDetail', on_delete=models.CASCADE, related_name='recruitment_requirement_detail_recruitment_tracking')