import random
from datetime import datetime
import pytz
from dateutil import tz

from employment_contracts.models import EmploymentContract
from rest_framework.views import exception_handler
from rest_framework import status
from rest_framework.utils.serializer_helpers import ReturnList
from django.utils.text import slugify
from base.constants.common import CodeConstants

from base.templates.error_templates import ErrorTemplate
from staffs.models import Staffs


def error_by_status_code(exc, response):
    if response.status_code == status.HTTP_403_FORBIDDEN:
        response.data['code'] = 'PERMIS_1'
        # response.data['message'] = ErrorTemplate.AuthorizedError.INCORRECT_AUTH_CRED['message']
    if response.status_code == status.HTTP_401_UNAUTHORIZED:
        response.data['code'] = ErrorTemplate.AuthorizedError.UNAUTHORIZED['code']
        response.data['message'] = ErrorTemplate.AuthorizedError.UNAUTHORIZED['message']
    else:
        response.data['message'] = exc.detail


def get_error_return_list(error_dict):
    errors = []
    for key, value in error_dict.items():
        # append errors into the list
        if type(value) is list:
            errors.append("{} : {}".format(key, " ".join(value)))
        else:
            errors.append("{} : {}".format(key, value))
    return errors


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # check if exception has dict items
    # remove the initial value
    if response is not None and ('code' not in response.data or ('code' in response.data
                                                                 and type(response.data['code'])) is list):
        response.data = dict()

        # serve status code in the response
        response.data['code'] = 'PARA_1'

        # Initial error message
        if not hasattr(exc, 'detail'):
            if response.status_code == status.HTTP_404_NOT_FOUND:
                response.data['code'] = 'NOT_FOUND'
                response.data['message'] = 'Not found'
            return response
        if hasattr(exc.detail, 'items'):
            # add property errors to the response
            response.data['message'] = get_error_return_list(exc.detail)[0]
        elif type(exc.detail) is ReturnList:
            for detail in [detail for detail in exc.detail if detail]:
                # add property errors to the response
                response.data['message'] = get_error_return_list(detail)[0]
                break
        else:
            error_by_status_code(exc, response)
            
    return response


def print_value(*args):
    """ Print value inside special characters to watch the value clearly """
    print("\n")
    print("+"+ "===="*20 + "+")
    print("\n")
    print(*args)
    print("\n")
    print("+"+ "===="*20 + "+")
    print("\n")


def without_keys(dictionany, keys):
    """ Return a new dictionary without specific keys """
    return {x: dictionany[x] for x in dictionany if x not in keys}

def radom_number(min,max):
    n = random.randint(min,max)
    return n

def generate_staff(first_name, last_name, staff_number='', department=''):
    """ Generate staff for staff """
    
    slug = slugify(f"{department} {first_name} {last_name} {staff_number}")
    staff = Staffs.objects.filter(staff=slug).first()
    if not staff:
        return slug
    else:
        staff_number = radom_number(
            min = CodeConstants().StaffRandomConstant().MIN,
            max = CodeConstants().StaffRandomConstant().MAX,
        )
        return generate_staff(department, first_name, last_name, staff_number)

def generate_number_contract(department='', type='', staff=''):
    """ Generate number contract """
    contract = EmploymentContract.objects.all().count()
    number_contract = f"{department}-{type}-{staff}-{contract+1}"
    
    return number_contract

def without_keys(dictionany, keys):
    """ Return a new dictionary without specific keys """
    return {x: dictionany[x] for x in dictionany if x not in keys}
