# Python imports

# Application imports


class ErrorTemplate:
    # Application by Portal/App error templates here
    class AuthorizedError:
        # Incorrect Authentication credentials
        UNAUTHORIZED = dict(
            code='AUTH_0',
            message='Incorrect authentication credentials.'
        )

        INCORRECT_AUTH_CRED = dict(
            code='AUTH_1',
            message="The username/password you've entered in incorrect, please try again."
        )

        # User Role Required
        ADMIN_REQUIRED = dict(
            code='AUTH_2',
            message='Admin required.'
        )

        USER_REQUIRED = dict(
            code='AUTH_3',
            message='User required.'
        )

        EMAIL_CONFIRM_REQUIRED = dict(
            code='AUTH_4',
            message='Account email confirmation is required.'
        )

        USER_ACTIVE_REQUIRED = dict(
            code='AUTH_5',
            message='Account activation is required.'
        )

        STAFF_REQUIRED = dict(
            code='AUTH_6',
            message='Required Staff User'
        )

        WRONG_PHONE_NUMBER = dict(
            code='AUTH_7',
            message='Wrong phone number, must be in format +xxxxxxxxxxxx'
        )

        OLD_PASS_WRONG = dict(
            code='AUTH_8',
            message='Old password is not correct.'
        )

        PASS_NOT_MATCH = dict(
            code='AUTH_9',
            message='Password does not match.'
        )

        NEW_PASS_SAME_OLD_PASS = dict(
            code='AUTH_10',
            message='New password should not be same old password.'
        )

        FILE_CANNOT_NULL = dict(
            code='AUTH_11',
            message='File is required.'
        )

        IS_VERIFIED = dict(
            code='AUTH_12',
            message='Your account is verified before or cannot found!'
        )

        FAILED_VERIFY_EMAIL = dict(
            code='AUTH_13',
            message='Failed to verify this email.'
        )

        USER_NOT_EXISTED = dict(
            code='AUTH_14',
            message='Cannot found user account! Please try again'
        )

        KEY_IS_EXPIRED = dict(
            code='AUTH_15',
            message='Verification code is expired. Please try again'
        )

        WRONG_RESET_PASSWORD_CODE = dict(
            code='AUTH_16',
            message='Wrong reset password code'
        )
        
        USER_EXISTED = dict(
            code='AUTH_17',
            message='The user already existed. Do you want to login!'
        )

        PHONE_CONFIRM_REQUIRED = dict(
            code='AUTH_18',
            message='Account phone number confirmation is required.'
        )
        
        HRM_REQUIRED = dict(
            code='AUTH_19',
            message='Hrm required.'
        )

    class UserError:
        USER_NOT_EXIST = dict(
            code='USER_1',
            message='User does not exist.'
        )

        PHONE_IS_USED = dict(
            code='USER_2',
            message='Phone has been used.'
        )

        EMAIL_IS_USED = dict(
            code='USER_3',
            message='Email has been used.'
        )

    class AdminError:
        USER_NOT_EXIST = dict(
            code='ADMIN_1',
            message='User is not existed.'
        )

        USER_IS_NOT_STAFF = dict(
            code='ADMIN_2',
            message='User is not Staff.'
        )

        STAFF_EXISTED = dict(
            code='STAFF_00',
            message='Already existed an user with this email or phone number.'
        )

        ROLE_EXISTED = dict(
            code='ROLE_00',
            message='This role was already existed.'
        )

        STAFF_NOT_FOUND = dict(
            code='STAFF_0',
            message='This staff can not found.'
        )

        ROLE_NOT_FOUND = dict(
            code='ROLE_0',
            message='This role can not be found.'
        )

    class PermissionError:
        @staticmethod
        def create_permission_denied_error(permission):
            parameter_error = dict(
                code='PERM_1',
                message='Required permission {}'.format(permission)
            )  # 403
            return parameter_error

    # Other error templates
    class CognitoError:
        USER_ALREADY_EXIST_ERROR = dict(
            code='COGNITO_1',
            message='User already exists.'
        )  # 400

        USER_NOT_CONFIRM_ERROR = dict(
            code='COGNITO_2',
            message='User email confirmation required.'
        )  # 400

        @staticmethod
        def create_cognito_error(message):
            cognito_error = dict(
                code='COGNITO_3',
                message=message
            )  # 400
            return cognito_error

    class ParameterError:
        @staticmethod
        def create_parameter_error(message):
            parameter_error = dict(
                code='PARA_1',
                message=message
            )  # 400
            return parameter_error

    class UUIDError:
        @staticmethod
        def uuid_error(message):
            uuid_error = dict(
                code='UUID_1',
                messgae=message
            )  # 400
            return uuid_error

    class StripeError:
        @staticmethod
        def webhook_error(error):
            parameter_error = dict(
                code='stripe_1',
                message='{}'.format(error)
            )  # 400
            return parameter_error

        INVALID_YEAR = dict(
            code='stripe_2',
            message='Your year of the birth day must be greater than or equal 1900'
        )

        @staticmethod
        def stripe_error(error):
            parameter_error = dict(
                code='stripe_3',
                message=''.format(error)
            )  # 400
            return parameter_error
    
    class Upload:
        def INVALID_FILE_EXTENSION (allow_extension):
            return dict(
                code="upload_1",
                message="Invalid file extensions: " + ", ".join(allow_extension)
            )