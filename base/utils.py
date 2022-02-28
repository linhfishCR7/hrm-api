from rest_framework.views import exception_handler
from rest_framework import status
from rest_framework.utils.serializer_helpers import ReturnList

from base.templates.error_templates import ErrorTemplate


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