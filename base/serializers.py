# Rest framework imports
from rest_framework import serializers
# Application imports
# Base imports
from base.constants.common import AppConstants
from base.services.image_handler import ImageHandler
# Serializer imports

# Model imports
from base.constants.common import AppConstants


class CommonSerializer(serializers.Serializer):
    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    @staticmethod
    def get_common_exclude_fields():
        return [
            "is_active",
            "created_by",
            "modified_at",
            "modified_by",
            "deleted_at",
            "deleted_by"
        ]


class FilterDateRangeFormatSerializer(CommonSerializer):
    from_date = serializers.DateField(required=False, allow_null=True, input_formats=['%Y-%m-%d'])
    to_date = serializers.DateField(required=False, allow_null=True, input_formats=['%Y-%m-%d'])

    class Meta:
        fields = (
            'from_date',
            'to_date',
        )


# Application Base Serializers
class ApplicationMethodFieldSerializer(CommonSerializer):

    @staticmethod
    def get_list_image(image):
        image_handler = ImageHandler()
        result = dict()
        url = image_handler.generate(image)
        result['image_s3_url'] = url

        list_image_size = []
        size = []
        for item in AppConstants.ImageSize.__dict__.items():
            if '__' not in item[0]:
                list_image_size.append(item[1][1])
                size.append(item[1][0][0])
        image_size_dict = {value: key for key, value in dict(list_image_size).items()}

        image_sizes = dict()
        for index in range(len(size)):
            url_resize = image_handler.generate(image, width=str(size[index]))
            image_dict = dict(
                height=0,
                width=size[index],
                image_s3_url=url_resize
            )
            image_sizes[image_size_dict[index]] = image_dict
        result['image_size'] = image_sizes
        result['image_key'] = image
        return result

    @staticmethod
    def get_video_url(video):
        image_handler = ImageHandler()
        result = dict()
        url = image_handler.generate(video)
        result['video_s3_url'] = url
        result['video_key'] = video
        return result


class UserBaseMethodsSerializer(CommonSerializer):

    @staticmethod
    def get_list_images(instance):
        if instance.image:
            image = ApplicationMethodFieldSerializer().get_list_image(instance.image)
            return image
        return None
    

class BaseUploadFileSerializer(CommonSerializer):
    file_type = serializers.ChoiceField(choices=AppConstants.Upload.FILE_OPTIONS)
    file_name = serializers.CharField(required=False)


class UploadResourceSerializer(CommonSerializer):
    file_name = serializers.CharField(required=False)

class FilteredSoftDeleteSerializer(serializers.ListSerializer):

    def to_representation(self, data):
        data = data.filter(is_deleted=False)
        return super(FilteredSoftDeleteSerializer, self).to_representation(data)


class MediaModelSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        response = super().to_representation(instance)
        
        if 'image' in response and response['image']:
            response['image'] = ApplicationMethodFieldSerializer.get_list_image(instance.image) 

        if 'video' in response and response['video']:
            response['video'] = ApplicationMethodFieldSerializer.get_video_url(instance.video)

        return response