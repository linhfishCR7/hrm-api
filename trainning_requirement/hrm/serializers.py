from trainning_requirement.models import TrainningRequirement
from branchs.models import Branchs
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


class TrainningRequirementSerializer(serializers.ModelSerializer):

    class Meta:
        model = TrainningRequirement
        fields = [
            "id",
            "date_requirement",
            "content",
            "course_name",
            "organizational_units",
            "time_organizational",
            "estimated_cost",
            "place",
            "sign_by",
            "unit_head",
            "approved_by",
            "unit",
            "branch",

        ]
        
    
class RetrieveAndListTrainningRequirementSerializer(serializers.ModelSerializer):
    branch = BranchSerializer(read_only=True)

    class Meta:
        model = TrainningRequirement
        fields = [
            "id",
            "date_requirement",
            "content",
            "course_name",
            "organizational_units",
            "time_organizational",
            "estimated_cost",
            "place",
            "sign_by",
            "unit_head",
            "approved_by",
            "unit",
            "branch",

        ]