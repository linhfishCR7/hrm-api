# Python imports
from base64 import b64encode
import json

# Django imports
from django.conf import settings

from base.services.s3_services import MediaUpLoad


class ImageConstants:
    EDIT_MODE = ['flip', 'flop', 'flatten', 'grayscale']

    class ResizeMode:
        COVER = 'cover'
        CONTAIN = 'contain'
        FILL = 'fill'
        INSIDE = 'inside'
        OUTSIDE = 'outside'


class ImageHandler:
    def __init__(self):
        self.url = settings.S3_URL
        self.bucket = settings.S3_BUCKET_NAME

    def generate(self, image='',  width='', height='', mode=ImageConstants.ResizeMode.COVER, edit_options=''):
        if self.url == '':
            return MediaUpLoad().get_image_url(image)
        
        # request = {
        #     'bucket': self.bucket,
        #     'key': image,
        #     'edits': {
        #     }
        # }
        # if width != '' and height != '':
        #     request['edits']['resize'] = {
        #         "width": width,
        #         "height": width,
        #         "fit": mode
        #     }
        # if edit_options != '':
        #     for edit in edit_options:
        #         if edit in ImageConstants.EDIT_MODE:
        #             request['edits'][edit] = True

        return f'{self.url}/{image}'
        # return f'{self.url}/{b64encode(json.dumps(request).encode()).decode()}'
