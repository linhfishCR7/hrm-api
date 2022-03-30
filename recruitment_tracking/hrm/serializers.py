from base.serializers import ApplicationMethodFieldSerializer
from recruitment_requirement_details.models import RecruitmentRequirementDetail
from recruitment_tracking.models import RecruitmentTracking
from rest_framework import serializers


class RecruitmentRequirementDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = RecruitmentRequirementDetail
        fields = [
            "id",
            "time_to_finish",
            "content",
            "position_requirement",
            "amount",
            "recuitment_requirement"
        ]


class RecruitmentTrackingSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = RecruitmentTracking
        fields = [
            "id",
            "position_recruiment",
            "date_receive_receipt_of_application",
            "is_job_application",
            "is_cv",
            "is_diploma",
            "is_health_certification",
            "office_day01",
            "is_qualification01",
            "office_day02",
            "is_qualification02",
            "is_agree_recruiment",
            "contact_before_sign_contract",
            "date_start_work",
            "salary_start",
            "is_receive_recruing_decision",
            "date_receive_recruing_decision",
            "recruitment_requirement_details"
        ]
        
    
class RetrieveAndListRecruitmentTrackingSerializer(serializers.ModelSerializer):
    recruitment_requirement_details = RecruitmentRequirementDetailSerializer()

    class Meta:
        model = RecruitmentTracking
        fields = [
            "id",
            "position_recruiment",
            "date_receive_receipt_of_application",
            "is_job_application",
            "is_cv",
            "is_diploma",
            "is_health_certification",
            "office_day01",
            "is_qualification01",
            "office_day02",
            "is_qualification02",
            "is_agree_recruiment",
            "contact_before_sign_contract",
            "date_start_work",
            "salary_start",
            "is_receive_recruing_decision",
            "date_receive_recruing_decision",
            "recruitment_requirement_details"
        ]