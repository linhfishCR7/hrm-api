# Python imports
from botocore.exceptions import (
    ClientError,
    ParamValidationError,
    UnknownParameterError,
    MissingParametersError,
)
import uuid

import stripe
from stripe import error
from django.conf import settings

# Django imports

# Rest framework imports
from rest_framework.exceptions import ValidationError

# Application imports
from base.templates.error_templates import ErrorTemplate
from users.models import User



# Validate UUID error handler
def check_uuid(key, uuid_str):
    try:
        uuid.UUID(uuid_str, version=4)
    except ValueError:
        message = '{} is not in UUID4 format'.format(key)
        raise ValidationError(ErrorTemplate.UUIDError.uuid_error(message))

def uuid_error_handler(func):
    def check_and_call(self, *args, **kwargs):
        if 'user_id' in self.kwargs:
            check_uuid('user_id', self.kwargs['user_id'])
            if not User.objects.filter(
                    id=self.kwargs.get('user_id'),
                    is_deleted=False
            ).exists():
                error = ErrorTemplate.UserError.USER_NOT_EXIST
                raise ValidationError(error)

        return func(self, *args, **kwargs)
    return check_and_call



# STRIPE
def stripe_error_handler(func):
    def check_and_call(*args, **kwargs):
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            return func(*args, **kwargs)

        except stripe.error.CardError as e:
            # Since it's a decline, stripe.error.CardError will be caught
            body = e.json_body
            err = body.get('error', {})
            raise ValidationError(dict(error=err.get('message')))

        except stripe.error.RateLimitError as e:
            # Too many requests made to the API too quickly
            body = e.json_body
            err = body.get('error', {})
            raise ValidationError(dict(error=err.get('message')))

        except stripe.error.InvalidRequestError as e:
            body = e.json_body
            err = body.get('error', {})
            print(dict(error=err.get('message')))
            raise ValidationError(dict(error=err.get('message')))

        except stripe.error.AuthenticationError as e:
            body = e.json_body
            err = body.get('error', {})
            raise ValidationError(dict(error=err.get('message')))

        except stripe.error.APIConnectionError as e:
            body = e.json_body
            err = body.get('error', {})
            raise ValidationError(dict(error=err.get('message')))

        except stripe.error.StripeError as e:
            body = e.json_body
            err = body.get('error', {})
            print(dict(error=err.get('message')))
            raise ValidationError(dict(error=err.get('message')))
    return check_and_call