"""
Service for upload and get media on AWS S3
"""

# Python imports
import base64
import hashlib
import hmac
import os
import uuid
import boto3
import mimetypes

# Django imports
from django.conf import settings
from django.utils import timezone

# Rest framework imports
from rest_framework.exceptions import ValidationError

# Application imports
from base.constants.common import AppConstants
from base.templates.error_templates import ErrorTemplate

from botocore.config import Config

from base.utils import print_value


class MediaUpLoad:
    s3_url = 'https://s3-{0}.amazonaws.com/{1}/{2}'
    s3 = boto3.resource('s3', aws_access_key_id=settings.S3_ACCESS_KEY, aws_secret_access_key=settings.S3_SECRET_KEY)
    s3_client = boto3.client(
        's3',
        config=Config(
            signature_version='s3v4',
            region_name=settings.S3_REGION
        ),
        region_name=settings.S3_REGION,
        aws_access_key_id=settings.S3_ACCESS_KEY,
        aws_secret_access_key=settings.S3_SECRET_KEY
    )

    def upload_media_to_s3(self, file):
        # Begin upload
        file_name, file_extension = os.path.splitext(file.name)
        file_extension = file_extension.lower()
        file_types = AppConstants.Upload.FILE_TYPES

        if file_extension not in file_types:
            raise ValidationError(ErrorTemplate.ParameterError.create_parameter_error(
                "File type is not valid, valid types: {0}.".format(", ".join(file_types))
            ))

        # Validate file size
        if file.size > AppConstants.Upload.MAX_FILE_SIZE:
            raise ValidationError(ErrorTemplate.ParameterError.create_parameter_error(
                "File size is too large, max: {0}.".format(AppConstants.Upload.MAX_FILE_SIZE)
            ))

        # Begin upload
        key = self.upload_file_to_s3(file, file_extension)

        return key


    def get_image_url(self, key):
        url = self.s3_url.format(settings.S3_REGION, settings.S3_BUCKET_NAME, key)
        return url

    def presign_url(self, key, file_extension, file_type):
        mime_type = mimetypes.guess_type(str(key))
        print_value(mime_type)
        if file_extension in ['.vrx', '.pvt']:
            content_type = 'application/octet-stream'
        elif file_extension in ['.heic']:
            content_type = 'image/heic'
        elif file_extension in ['.heif']:
            content_type = 'image/heif'
        else:
            content_type = mime_type[0]

        response = self.s3_client.generate_presigned_post(
                settings.S3_BUCKET_NAME,
                key,
                ExpiresIn=604800,
                Fields={"Content-Type": content_type},
                Conditions=[
                    ["starts-with", "$Content-Type", content_type]],
            )
        return response

    @staticmethod
    def get_media_upload_policy(file_object, file_name, upload_start_path):  # Using for upload multiple files
        now = timezone.now() + timezone.timedelta(minutes=30)
        policy_expires = "{}-{}-{}T{}:{}:{}Z".format(now.year, now.month, now.day, now.hour, now.minute, now.second)

        policy_document_context = {
            "expire": policy_expires,
            "bucket_name": settings.S3_BUCKET_NAME,
            "key_name": "",
            "acl_name": "public-read",
            "content_name": "",
            "content_length": 524288000,
            "upload_start_path": upload_start_path
        }
        policy_document = """
                            {
                                "expiration: "%(expire)s",
                                "conditions": [
                                    {"bucket": "%%(bucket_name)s"},
                                    ["starts-with", "$key", "%(upload_start_path)s"],
                                    {"acl": "%(acl_name)s"},
                                    ["starts-with", "$Content-Type", "%(content_name)s"],
                                    ["starts-with", "$filename", ""],
                                    ["content-length-range", 0, %(content_length)d]
                                ]
                            }
                            """ % policy_document_context
        aws_secret = str.encode(settings.S3_SECRET_KEY)
        policy_document_str_encoded = str.encode(policy_document.replace("", ""))

        s3_url = "https://s3-{0}.amazonaws.com/{1}/".format(
            settings.S3_REGION,
            settings.S3_BUCKET_NAME
        )

        policy = base64.b64encode(policy_document_str_encoded)
        signature = base64.b64encode(hmac.new(aws_secret, policy, hashlib.sha1).digest())
        data = {
            "policy": policy,
            "signature": signature,
            "key": settings.S3_ACCESS_KEY,
            "file_bucket_path": upload_start_path,
            "file_id": file_object.id,
            "filename": file_name,
            "url": s3_url
        }

        return data

    def presign_image_url(self, key):
        mime_type = mimetypes.guess_type(str(key))
        content_type = mime_type[0]
        links = boto3.client(
            's3', aws_access_key_id=settings.S3_ACCESS_KEY, aws_secret_access_key=settings.S3_SECRET_KEY,
            config=Config(
                signature_version='s3v4',
                region_name=settings.S3_REGION
            ),
            region_name=settings.S3_REGION
        ).generate_presigned_post(
            settings.S3_BUCKET_NAME,
            key,
            ExpiresIn=300,
             Fields={"Content-Type": content_type},
                Conditions=[
                    ["starts-with", "$Content-Type", content_type]],
        )
        return links

    def upload_pdf_to_s3(self, file_path, key):
        key = str(uuid.uuid4())[:12] + '_' + key
        try:
            self.s3.Bucket(settings.S3_BUCKET_NAME).upload_file(
                Key=key,
                Filename=file_path,
                ExtraArgs={
                    'ACL': 'public-read',
                    'ContentType': 'application/pdf'
                },
            )
            return key
        except Exception as e:
            raise e
    
    def get_file_url(self, key):
        url = self.s3_url.format(settings.S3_REGION, settings.S3_BUCKET_NAME, key)
        return url