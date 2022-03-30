from sre_constants import BRANCH
from base.serializers import ApplicationMethodFieldSerializer
from departments.models import Departments
from recruitment_requirements.models import RecruitmentRequirement
from branchs.models import Branchs
from staffs.models import Staffs
from users.models import User
from rest_framework import serializers


class BranchSerializer(serializers.ModelSerializer):

    class Meta:
        model = Branchs
        fields = [
            'id',
            'branch',
            'name',
        ]
        read_only_fields = ['id']


class DepartmentSerializer(serializers.ModelSerializer):
    branch = BranchSerializer(read_only=True)
    class Meta:
        model = Departments
        fields = [
            'id',
            'department',
            'name',
            'branch'
        ]
        read_only_fields = ['id']


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
        
    
class RetrieveAndListRecruitmentRequirementSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer()

    class Meta:
        model = RecruitmentRequirement
        fields = [
            'id',
            'created_at_recruitment',
            'approved_by',
            'asked_by',
            'department'

        ]