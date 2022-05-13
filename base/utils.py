import random
import string
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

## characters to generate password from
alphabets = list(string.ascii_letters)
digits = list(string.digits)
special_characters = list("!@#$%^&*()")
characters = list(string.ascii_letters + string.digits + "!@#$%^&*()")

def generate_random_password():

	## initializing the password
	password = []

	## picking random alphabets
	for i in range(4):
		password.append(random.choice(alphabets))

	## picking random digits
	for i in range(4):
		password.append(random.choice(digits))

	## picking random alphabets
	for i in range(4):
		password.append(random.choice(special_characters))

	## shuffling the resultant password
	random.shuffle(password)

	## converting the list to string
	## printing the list
	return("".join(password))

    
# from io import BytesIO
# from django.http import HttpResponse
# from django.template.loader import get_template

# from xhtml2pdf import pisa

# def render_to_pdf(template_src, context_dict={}):
#     template = get_template(template_src)
#     html  = template.render(context_dict)
#     result = BytesIO()
#     pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
#     if not pdf.err:
#         return HttpResponse(result.getvalue(), content_type='application/pdf')
#     return None
# import csv

# @staticmethod
# def export_to_csv(export_result, filename, fair, from_date, to_date):
#     response = HttpResponse(content_type='text/csv')
#     response['Content-Disposition'] = 'attachment; filename={}.csv'.format(filename)
#     writer = csv.writer(response, csv.excel)
#     response.write(u'\ufeff'.encode('utf8'))
#     # with open('market_report.csv', 'w', newline='') as file:
#     #     writer = csv.writer(file, csv.excel)
#     writer.writerow([
#         smart_str(u"From"),
#         smart_str(u"{}".format(from_date)),
#         smart_str(u"To"),
#         smart_str(u"{}".format(to_date))
#     ])
#     writer.writerow([
#         smart_str(u"Market"),
#         smart_str(fair.name)
#     ])

#     # Offline session
#     offline_sales = export_result['offline_sales']
#     # Header
#     writer.writerow([
#         smart_str(u"Total Stalls"),
#         smart_str(u"Total Rent Invoiced"),
#         smart_str(u"Total Hosts"),
#         smart_str(u"EFTPOS"),
#         smart_str(u"Commission"),
#         smart_str(u"Surcharge"),
#         smart_str(u"Conditional Surcharge"),
#         smart_str(u"Total"),
#         # smart_str(u"EFTPOS and Card"),
#         smart_str(u"Cash"),
#         smart_str(u"Voucher Spent"),
#         smart_str(u"Voucher Created"),
#         smart_str(u"Total Voucher"),
#         smart_str(u"Total Payment"),
#     ])
#     # Value
#     writer.writerow([
#         smart_str(offline_sales['total_stalls']),
#         smart_str(offline_sales['total_rent_invoiced']),
#         smart_str(''),
#         smart_str(offline_sales['eftpos_total']),
#         smart_str(offline_sales['eftpos_commission']),
#         smart_str(offline_sales['eftpos_surcharge'].quantize(decimal.Decimal('0.01'))),
#         smart_str(offline_sales['eftpos_conditional_surcharge'].quantize(decimal.Decimal('0.01'))),
#         smart_str(offline_sales['eftpos_total'].quantize(decimal.Decimal('0.01'))),
#         # smart_str(offline_sales['eftpos_and_card'].quantize(decimal.Decimal('0.01'))),
#         smart_str(offline_sales['cash'].quantize(decimal.Decimal('0.01'))),
#         smart_str(offline_sales['voucher_created'].quantize(decimal.Decimal('0.01'))),
#         smart_str(offline_sales['voucher_unspent']),
#         smart_str(offline_sales['voucher'].quantize(decimal.Decimal('0.01'))),
#         smart_str(offline_sales['total_sales'].quantize(decimal.Decimal('0.01'))),
#     ])
#     # Count
#     writer.writerow([
#         smart_str(u""),
#         smart_str(u""),
#         smart_str(u""),
#         smart_str(u""),
#         smart_str(u""),
#         # smart_str(offline_sales['total_stalls']),
#         smart_str(u""),
#         # smart_str(offline_sales['total_hosts']),
#         # smart_str(offline_sales['eftpos_count']),
#         smart_str(u""),
#         smart_str(u""),
#         # smart_str(offline_sales['eftpos_conditional_surcharge_count']),
#         smart_str(offline_sales['eftpos_total']),
#         smart_str(offline_sales['cash_count']),
#         smart_str(offline_sales['voucher_count']),
#         # smart_str(offline_sales['payment_count']),
#     ])
#     return response

 


