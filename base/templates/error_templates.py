from django.core.checks import messages


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
            message="The phone/password you've entered in incorrect, please try again."
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

        NOT_VERIFY_PHONE = dict(
            code='AUTH_5',
            message='Account must be verified phone before'
        )

        USER_EXISTED = dict(
            code='AUTH_6',
            message='An account already existed by this phone number'
        )

        WRONG_PHONE_NUMBER_FORMAT = dict(
            code='AUTH_7',
            message='Wrong phone number, must be in format +xxxxxxxxxxxx'
        )

        USER_NOT_EXISTED = dict(
            code='AUTH_8',
            message='Cannot found user account! Please try again'
        )
    
    class UUIDError:
        @staticmethod
        def uuid_error(message):
            uuid_error = dict(
                code='UUID_1',
                messgae=message
            )  # 400
            return uuid_error

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

    class ValueFormatError():
        def NOT_JSON_FORMAT(self, value):
            return dict(
                code="value_0",
                message = f"{value} is not a json format"
            )

        def JSON_FORMAT_WRONG(self, value):
            return dict(
                code="value_1",
                message=f"{value} not contain keys required"
            )
