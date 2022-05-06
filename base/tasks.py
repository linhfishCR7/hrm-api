from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings

from celery import shared_task
from base.constants.common import NotificationType

from base.services.mail_services import email_service
from base.templates.email_templates import BaseTemplate, EmailTemplate
from base.services.firebase_services import FirebaseNotificationService
from base.templates.notification_template import NotificationTemplate
from base.utils import print_value
from salaries.models import Salary
from staffs.models import Staffs
from users.models import User, UserFCMDevice
from notification.models import Notification

fcm_client = FirebaseNotificationService()


@shared_task(bind=True)
def welcome_email(self, data):
    email_from = settings.DEFAULT_FROM_EMAIL
    message = BaseTemplate.BASE.format(
            year=timezone.now().year,
            section=EmailTemplate.WelcomeEmail.BODY(data['name'])
        )
    subject = str(EmailTemplate.WelcomeEmail.SUBJECT)
    recipient_list = [data['email'],]
    email_service(email_from=email_from, message=message, subject=subject, recipient_list=recipient_list)


@shared_task(retries=3)
def push_admin_notification_account_created(metadata, name):
    """ Send notification to all admin after the account has been created """

    """ Find admin user registration ids """
    admin_user_registration_ids = UserFCMDevice.objects.filter(
        user__is_staff=True,
        user__is_superuser=True,
        is_deleted=False,
        is_active=True
    ).values_list("token", flat=True)

    notification_title = NotificationTemplate.UserCreated.TITLE(name)
    notification_body = NotificationTemplate.UserCreated.BODY
    notification_type = NotificationType.NEW_USER

    """ Push notification to admins  """
    fcm_client.send_notification_multiple_user(
        list_registration_id=admin_user_registration_ids,
        title=notification_title,
        body=notification_body
    )

    """ Find admin users """
    admins = User.objects.filter(
        is_staff=True,
        is_superuser=True,
        is_deleted=False,
        is_active=True
    )
    notification_data = [
        Notification(
            user=admin,
            title=notification_title,
            body=notification_body,
            notification_type=notification_type,
            metadata={"user_id": str(metadata)}
        ) for admin in admins
    ]

    """ Add notification to database """
    Notification.objects.bulk_create(notification_data)    
    return True


@shared_task(bind=True)
def day_off_year_email(self, data):
    email_from = settings.DEFAULT_FROM_EMAIL
    link = f"{settings.FRONTEND_URL}day-off-year/{data['link']}"
    message = BaseTemplate.BASE.format(
            year=timezone.now().year,
            section=EmailTemplate.DayOffYearEmail.BODY(name=data['name'], link=link)
        )
    subject = str(EmailTemplate.DayOffYearEmail.SUBJECT)
    hrms = User.objects.filter(
        is_staff=True,
        is_deleted=False,
        is_active=True
    ).values_list('email', flat=True)
     
    recipient_list = hrms
    email_service(email_from=email_from, message=message, subject=subject, recipient_list=recipient_list)


@shared_task(retries=3)
def push_hrn_notification_user_created_day_off_year(metadata, name):
    """ Send notification to all hrm after the user has been created day off year"""

    """ Find hrm user registration ids """
    hrm_registration_ids = UserFCMDevice.objects.filter(
        user__is_staff=True,
        user__is_superuser=False,
        is_deleted=False,
        is_active=True
    ).values_list("token", flat=True)

    notification_title = NotificationTemplate.UserCreateDayOffYear.TITLE(name)
    notification_body = NotificationTemplate.UserCreateDayOffYear.BODY
    notification_type = NotificationType.USER_CREATED_DAY_OF_YEAR

    """ Push notification to hrms  """
    fcm_client.send_notification_multiple_user(
        list_registration_id=hrm_registration_ids,
        title=notification_title,
        body=notification_body
    )

    """ Find hrm users """
    hrms = User.objects.filter(
        is_staff=True,
        is_superuser=False,
        is_deleted=False,
        is_active=True
    )
    notification_data = [
        Notification(
            user=hrm,
            title=notification_title,
            body=notification_body,
            notification_type=notification_type,
            metadata={"user_id": str(metadata)}
        ) for hrm in hrms
    ]

    """ Add notification to database """
    Notification.objects.bulk_create(notification_data)    
    return True


@shared_task(bind=True)
def day_off_year_email_to_user(self, data):
    email_from = settings.DEFAULT_FROM_EMAIL
    link = f"{settings.FRONTEND_URL}day-off-year/{data['link']}"
    message = BaseTemplate.BASE.format(
            year=timezone.now().year,
            section=EmailTemplate.DayOffYearEmailToUser.BODY(name=data['name'], link=link)
        )
    subject = str(EmailTemplate.DayOffYearEmailToUser.SUBJECT)
    user = User.objects.filter(
        id=data['user_id'],
        is_deleted=False,
        is_active=True
    ).values_list('email', flat=True)
     
    recipient_list = user
    email_service(email_from=email_from, message=message, subject=subject, recipient_list=recipient_list)


@shared_task(bind=True)
def day_off_year_refuse_email_to_user(self, data):
    email_from = settings.DEFAULT_FROM_EMAIL
    link = f"{settings.FRONTEND_URL}day-off-year/{data['link']}"
    message = BaseTemplate.BASE.format(
            year=timezone.now().year,
            section=EmailTemplate.DayOffYearRefuseEmailToUser.BODY(name=data['name'], link=link)
        )
    subject = str(EmailTemplate.DayOffYearRefuseEmailToUser.SUBJECT)
    user = User.objects.filter(
        id=data['user_id'],
        is_deleted=False,
        is_active=True
    ).values_list('email', flat=True)
     
    recipient_list = user
    email_service(email_from=email_from, message=message, subject=subject, recipient_list=recipient_list)


@shared_task(retries=3)
def push_user_notification_hrm_approved_day_off_year(metadata, user_id):
    """ Send notification to all user after the hrm has been approved day off year"""

    """ Find hrm user registration ids """
    user_registration_ids = UserFCMDevice.objects.filter(
        user_id=user_id,
        is_deleted=False,
        is_active=True
    ).values_list("token", flat=True)

    notification_title = NotificationTemplate.HrmApprovedDayOffYear.TITLE
    notification_body = NotificationTemplate.HrmApprovedDayOffYear.BODY
    notification_type = NotificationType.HRM_APPROVED_DAY_OF_YEAR

    """ Push notification to hrms  """
    fcm_client.send_notification_multiple_user(
        list_registration_id=user_registration_ids,
        title=notification_title,
        body=notification_body
    )

    """ Find hrm users """
    users = User.objects.filter(
        id=user_id,
        is_deleted=False,
        is_active=True
    )
    notification_data = [
        Notification(
            user=user,
            title=notification_title,
            body=notification_body,
            notification_type=notification_type,
            metadata={"user_id": str(metadata)}
        ) for user in users
    ]

    """ Add notification to database """
    Notification.objects.bulk_create(notification_data)    
    return True


@shared_task(retries=3)
def push_user_notification_hrm_refused_day_off_year(metadata, user_id):
    """ Send notification to all user after the hrm has been refused day off year"""

    """ Find hrm user registration ids """
    user_registration_ids = UserFCMDevice.objects.filter(
        user_id=user_id,
        is_deleted=False,
        is_active=True
    ).values_list("token", flat=True)

    notification_title = NotificationTemplate.HrmRefusedDayOffYear.TITLE
    notification_body = NotificationTemplate.HrmRefusedDayOffYear.BODY
    notification_type = NotificationType.HRM_REFUSED_DAY_OF_YEAR

    """ Push notification to hrms  """
    fcm_client.send_notification_multiple_user(
        list_registration_id=user_registration_ids,
        title=notification_title,
        body=notification_body
    )

    """ Find hrm users """
    users = User.objects.filter(
        id=user_id,
        is_deleted=False,
        is_active=True
    )
    notification_data = [
        Notification(
            user=user,
            title=notification_title,
            body=notification_body,
            notification_type=notification_type,
            metadata={"user_id": str(metadata)}
        ) for user in users
    ]

    """ Add notification to database """
    Notification.objects.bulk_create(notification_data)    
    return True


@shared_task(bind=True)
def salary_email_to_all_user(self):
    email_from = settings.DEFAULT_FROM_EMAIL
    salary_staff = Salary.objects.filter(
        is_deleted=False,
        is_active=False,
        date__month=timezone.now().month-1,
        date__year=timezone.now().year
    ).values_list('staff', flat=True)
    print_value(salary_staff)
    staff_user = Staffs.objects.filter(
        is_deleted=False,
        id__in=salary_staff
    ).values_list('user', flat=True)
    print_value(staff_user)

    user = User.objects.filter(
        id__in=staff_user,
        is_deleted=False,
        is_active=True
    ).values()
    for data in user:
        # staff = Staffs.objects.filter(
        #     user_id=data['id']
        # ).get()
        # salary = Salary.objects.filter(
        #     staff_id=staff.id,
        #     is_deleted=False,
        #     date__month=timezone.now().month-1,
        #     date__year=timezone.now().year
        # ).values()

        message = BaseTemplate.BASE.format(
                year=timezone.now().year,
                section=EmailTemplate.SalaryEmailToAllUser.BODY(
                    name=f"{data['first_name']} {data['last_name']}", 
                    link=f"{settings.FRONTEND_URL}salary/"
                )
            )
        subject = EmailTemplate.SalaryEmailToAllUser.SUBJECT(month=timezone.now().month, year=timezone.now().year)
        
        
        recipient_list = [data['email']]
        email_service(email_from=email_from, message=message, subject=subject, recipient_list=recipient_list)


@shared_task(retries=3)
def push_all_user_notification_hrm_approved_send_salary(month=timezone.now().month, year=timezone.now().year):
    """ Send notification to all user after the hrm has been approved day off year"""

    """ Find all user registration ids but admin """
    salary_staff = Salary.objects.filter(
        is_deleted=False,
        is_active=False,
        date__month=timezone.now().month-1,
        date__year=timezone.now().year
    ).values_list('staff', flat=True)
    staff_user = Staffs.objects.filter(
        is_deleted=False,
        id__in=salary_staff
    ).values_list('user', flat=True)
    user_registration_ids = UserFCMDevice.objects.filter(
        id__in=staff_user,
        is_deleted=False,
        is_active=True
    ).values_list("token", flat=True)

    notification_title = NotificationTemplate.HrmSendSalaryToAllUser.TITLE(month, year)
    notification_body = NotificationTemplate.HrmSendSalaryToAllUser.BODY
    notification_type = NotificationType.HRM_SEND_SALARY_TO_ALL_USER

    """ Push notification to all user but admin  """
    fcm_client.send_notification_multiple_user(
        list_registration_id=user_registration_ids,
        title=notification_title,
        body=notification_body
    )

    """ All users but admin """
    users = User.objects.filter(
        id__in=staff_user,
    )
    notification_data = [
        Notification(
            user=user,
            title=notification_title,
            body=notification_body,
            notification_type=notification_type,
            metadata={}
        ) for user in users
    ]

    """ Add notification to database """
    Notification.objects.bulk_create(notification_data)    
    return True


@shared_task(retries=3)
def push_admin_notification_staff_deleted(metadata, name, email):
    """ Send notification to all admin after the profile has been deleted """

    """ Find admin user registration ids """
    admin_user_registration_ids = UserFCMDevice.objects.filter(
        user__is_superuser=True,
        is_deleted=False,
        is_active=True
    ).values_list("token", flat=True)

    notification_title = NotificationTemplate.ProfileDelete.TITLE(name)
    notification_body = NotificationTemplate.ProfileDelete.BODY(email)
    notification_type = NotificationType.HRM_SEND_STAFF_DELETED

    """ Push notification to admins  """
    fcm_client.send_notification_multiple_user(
        list_registration_id=admin_user_registration_ids,
        title=notification_title,
        body=notification_body
    )

    """ Find admin users """
    admins = User.objects.filter(
        is_superuser=True,
        is_deleted=False,
        is_active=True
    )
    notification_data = [
        Notification(
            user=admin,
            title=notification_title,
            body=notification_body,
            notification_type=notification_type,
            metadata={"user_id": str(metadata)}
        ) for admin in admins
    ]

    """ Add notification to database """
    Notification.objects.bulk_create(notification_data)    
    return True
