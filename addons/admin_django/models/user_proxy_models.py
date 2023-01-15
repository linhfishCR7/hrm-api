from users.models import User


class HrUserAdmin(User):

    class Meta:
        proxy = True
        verbose_name = 'Hr User'
        verbose_name_plural = 'Hr User'
        app_label = 'users'
