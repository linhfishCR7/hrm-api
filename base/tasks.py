from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings

from celery import shared_task
from base.constants.common import NotificationType

from base.services.mail_services import email_service
from base.templates.email_templates import BaseTemplate, EmailTemplate
from base.services.firebase_services import FirebaseNotificationService
from base.templates.notification_template import NotificationTemplate
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