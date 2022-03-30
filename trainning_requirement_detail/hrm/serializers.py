from base.serializers import ApplicationMethodFieldSerializer
from staffs.models import Staffs
from trainning_requirement.models import TrainningRequirement
from trainning_requirement_detail.models import TrainningRequirementDetail
from branchs.models import Branchs
from rest_framework import serializers
from users.models import User



class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = [
            'id',
            'first_name',
            'last_name',
            'image',
        ]
        read_only_fields = ['id']

    def to_representation(self, instance):
        """
        To show the data response to users
        """
        response = super().to_representation(instance)
        if instance.image:
            response['image'] = ApplicationMethodFieldSerializer.get_list_image(instance.image)
        
        return response


class StaffsSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Staffs
        fields = [
            'id',
            'staff',
            'user'
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
        read_only_fields = ['id']


class TrainningRequirementDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = TrainningRequirementDetail
        fields = [
            "id",
            "date",
            "amount",
            "note",
            "staff",
            "trainning_requirement",
        ]
        
    
class RetrieveAndListTrainningRequirementDetailSerializer(serializers.ModelSerializer):
    staff = StaffsSerializer(read_only=True)
    trainning_requirement = TrainningRequirementSerializer(read_only=True)

    class Meta:
        model = TrainningRequirementDetail
        fields = [
            "id",
            "date",
            "amount",
            "note",
            "staff",
            "trainning_requirement",
        ]