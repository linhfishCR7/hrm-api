"""
Service for Cognito User Pool authentication
"""

# Python imports
from botocore.exceptions import ClientError

# Django imports
from django.conf import settings

# Application imports
from base.services.warrant_cognito import Cognito
from base.decorators import cognito_error_handler
from base.utils import print_value


class CognitoService:

    class Authentication:
        @staticmethod
        def get_cognito_token(request):
            cognito_access_token = request.META.get('HTTP_COGNITO_USER_ACCESS_TOKEN')

            return cognito_access_token

    class User:
        def __init__(self):
            self.u = Cognito(
                user_pool_id=settings.COGNITO_USER_POOL,
                client_id=settings.COGNITO_AUDIENCE,
                # client_secret=settings.COGNITO_AUDIENCE_SECRET,
                user_pool_region=settings.COGNITO_AWS_REGION,
            )

        # @staticmethod
        @cognito_error_handler
        def register(self, email='', password='', phone_number='', username=None, custom_attributes={}):
            if custom_attributes:
                self.u.add_custom_attributes(
                    **custom_attributes
                )
            self.u.add_base_attributes(email=email)
            # user = None
            # if username:
            #     user = self.u.register(username, password)
            # else:
            #     user = self.u.register(email, password)
            user = self.u.register(email, password)
            return user
        

        # @staticmethod
        @cognito_error_handler
        def authenticate(self, username, password):
            self.u.username = username
            self.u.authenticate(password=password)

            result = dict(
                cognito_access_token=self.u.access_token,
                cognito_id_token=self.u.id_token,
            )

            return result

        @cognito_error_handler
        def send_verified_email_code(self, cognito_token):
            self.u.id_token = cognito_token['id_token']
            self.u.refresh_token = cognito_token['refresh_token']
            self.u.access_token = cognito_token['access_token']
            self.u.send_verification(attribute='email')

            return True

        @cognito_error_handler
        def confirm_verified_email_code(self, verified_code, username):
            self.u.confirm_sign_up(verified_code, username=username)

            return True

        @cognito_error_handler
        def resend_confirmation_email(self, username):
            self.u.resend_confirmation_code(username)

            return True

        @cognito_error_handler
        def get_user(self, username):
            self.u.username = username
            user = self.u.admin_get_user(attr_map={
                    "custom:first_name": "first_name",
                    "custom:last_name": "last_name",
                    "custom:hunter_bank_token": "hunter_bank_token",
                    "custom:hunter_maccount": "hunter_maccount",
                    "custom:acm_bank_token": "acm_bank_token",
                    "custom:acm_maccount": "acm_maccount",
                    "custom:admin_mfa_key": "mfa_key",
                    "custom:is_mfa": 'is_mfa'
                })

            return user

        @cognito_error_handler
        def delete_user(self, username):
            self.u.username = username
            self.u.admin_delete_user()

            return True

        @cognito_error_handler
        def forgot_password(self, username):
            self.u.username = username
            self.u.initiate_forgot_password()

            return True

        @cognito_error_handler
        def reset_password(self, username, reset_code, new_password):
            self.u.username = username
            self.u.confirm_forgot_password(reset_code, new_password)

            return True

        @cognito_error_handler
        def update_password(self, access_token, previous_password, proposed_password):
            self.u.access_token = access_token
            self.u.change_password(previous_password, proposed_password)

            return True

        """
        # Update user profile by Admin on Cognito
        Example:
        attributes_dict = {
            'custom:first_name': data['first_name'],
            'custom:last_name': data['last_name'],
            'custom:bank_token': data['bank_token'],
            'custom:maccount_number': data['maccount_number'],
            'custom:card_token': data['card_token'],
        }
        CognitoService.User().admin_update_user_attributes(
            username=request.user.username,
            attributes_dict=attributes_dict
        )
        """

        @cognito_error_handler
        def admin_update_user_attributes(self, username, attributes_dict):
            self.u.username = username
            self.u.admin_update_profile(attrs=attributes_dict)

            return True

        @cognito_error_handler
        def admin_confirm_sign_up(self, username):
            self.u.username = username
            self.u.admin_confirm_sign_up()

            return True

        def check_user_existed(self, username):
            self.u.username = username
            try:
                self.u.admin_get_user()
                return 1
            except ClientError as e:
                return 0

        @cognito_error_handler
        def admin_change_user_password(self, password, username=None):
            try:
                self.u.admin_set_user_password(password=password, username=username)
                return True
            except:
                return False
