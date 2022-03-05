# Python imports
from pyfcm import FCMNotification

# Django imports
from django.conf import settings

# Rest Framework import


class FirebaseNotificationService:

    def __init__(self):
        self.push_service = FCMNotification(api_key=settings.FCM_SERVER_KEY)

    def send_notification_single_uer(self, registration_id, title, body, extra=None):
        if not registration_id:
            return False

        result = self.push_service.notify_single_device(
            registration_id=registration_id,
            message_title=title,
            message_body=body,
            sound="default",
            extra_notification_kwargs=extra,
        )
        return result

    def send_notification_multiple_user(self, list_registration_id, title, body, extra=None):
        if not list_registration_id:
            return False

        for registration_id in list_registration_id:
            if registration_id:
                registration = registration_id.split(',')
                result = self.push_service.notify_multiple_devices(
                    registration_ids=registration,
                    message_title=title,
                    message_body=body,
                    sound="default",
                    extra_notification_kwargs=extra
                )
        return True


class FireBaseService:
    # Initiate Client for ESE send email
    def __init__(self, fcm_server_key=settings.FCM_SERVER_KEY):
        self.fcm_service = FCMNotification(api_key=fcm_server_key)

    # FireBase send notification base function
    def notify_to_multiple_devices(self, registration_ids, message_title, message_body, data_message=None):
        extra_kwargs = {
            'apns': {
                'headers': {
                    'apns-priority': '10',
                },
                'payload': {
                    'aps': {
                        'sound': 'default',
                    }
                },
            },
            'android': {
                'priority': 'high',
                'notification': {
                    'sound': 'default',
                }
            },
        }
        if data_message is None:
            response = self.fcm_service.notify_multiple_devices(
                registration_ids=registration_ids,
                message_title=message_title,
                message_body=message_body,
                extra_kwargs=extra_kwargs,
            )
        else:
            response = self.fcm_service.notify_multiple_devices(
                registration_ids=registration_ids,
                message_title=message_title,
                message_body=message_body,
                data_message=data_message,
                extra_kwargs=extra_kwargs,
            )

        return response
