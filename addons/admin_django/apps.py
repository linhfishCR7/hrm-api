from django.contrib.admin.apps import AdminConfig
from django.apps import AppConfig


class CustomAdminConfig(AdminConfig):
    default_site = 'addons.admin_django.admin.CustomAdminSite'


class CustomAdminAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'addons.admin_django'
