# Add menus of admin site here.
from .base import *

from .user_admin import *
from companies.models import Companies

# Register menus for admin site here.
admin_site.register(HrUserAdmin, HrAdmin)
