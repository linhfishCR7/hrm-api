from django.db import models
from base.models import BaseModel
from base.constants.common import NotificationType,NotificationMetadata

class Notification(BaseModel):
    """ Notification table """
    user = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="user_notifications")
    title = models.CharField(max_length=255, null=False, default=None)
    body = models.CharField(max_length=255, null=False, default=None)
    notification_type = models.IntegerField(default=NotificationType.NEW_USER)
    is_seen = models.BooleanField(default=False)
    metadata = models.JSONField(default=NotificationMetadata.default_data)