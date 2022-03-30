from sre_constants import BRANCH
from base.serializers import ApplicationMethodFieldSerializer
from branchs.models import Branchs
from recruitment_requirements.models import RecruitmentRequirement
from recruitment_requirement_details.models import RecruitmentRequirementDetail
from rest_framework import serializers


class RecruitmentRequirementSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecruitmentRequirement
        fields = [
            'id',
            'created_at_recruitment',
            'approved_by',
            'asked_by',
            'department'
        ]
        read_only_fields = ['id']


class RecruitmentRequirementDetailSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = RecruitmentRequirementDetail
        fields = [
            'id',
            'time_to_finish',
            'content',
            'position_requirement',
            'amount',
            'recuitment_requirement'

        ]
        

class RetrieveAndListRecruitmentRequirementDetailSerializer(serializers.ModelSerializer):
    recuitment_requirement = RecruitmentRequirementSerializer()

    class Meta:
        model = RecruitmentRequirementDetail
        fields = [
            'id',
            'time_to_finish',
            'content',
            'position_requirement',
            'amount',
            'recuitment_requirement'

        ]