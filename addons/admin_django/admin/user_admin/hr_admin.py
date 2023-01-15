import uuid

from django.contrib import admin
from django.contrib import messages
from django.utils import timezone

from .base_user_admin import CustomUserAdmin
from ...models import HrUserAdmin


class HrAdmin(CustomUserAdmin):
    model = HrUserAdmin
    actions = ['delete_staff_user', 'block_staff_user', 'unblock_staff_user']


    def get_queryset(self, request):
        return super().get_queryset(request).filter(
            is_staff=True,
        )

    def has_delete_permission(self, request, obj=None):
        return False

    # List View.
    list_display = ['email', 'is_verified_email', 'is_active', 'created_at']
    list_per_page = 10
    search_fields = ['first_name', 'last_name', 'email']
    ordering = ("-created_at",)
    sortable_by = ['email', 'created_at']
    list_filter = ['is_active', 'is_verified_email']

    @admin.action(description='Delete selected staff users')
    def delete_staff_user(self, request, queryset):
        try:
            # Check user has asigned to any projects
            list_saler_id = queryset.values_list('id', flat=True)
            Project.objects.filter(assigned_staff__in=list_saler_id).update(assigned_staff=None)
            queryset.update(
                is_deleted=True,
                deleted_at=timezone.now(),
                deleted_by=request.user.id,
            )
            self.message_user(request, "Successfully deleted staff users.", level=messages.SUCCESS)
        except Exception as e:
            self.message_user(request, "Failed to delete staff users. Error: {}".format(e), level=messages.ERROR)

    def save_model(self, request, obj, form, change):
        if not change:
            obj.is_verified_email = True
            obj.is_staff_user = True
            obj.username = uuid.uuid4()
        return super().save_model(request, obj, form, change)
        # Send email to user. Include email and password.

    @admin.action(description='Block selected staff users')
    def block_staff_user(self, request, queryset):
        #TODO send email to staff user
        queryset.update(is_active=False)
        self.message_user(request, "Successfully blocked staff users.", level=messages.SUCCESS)

    @admin.action(description='Unblock selected staff users')
    def unblock_staff_user(self, request, queryset):
        #TODO send email to staff user
        queryset.update(is_active=True)
        self.message_user(request, "Successfully unblocked staff users.", level=messages.SUCCESS)
