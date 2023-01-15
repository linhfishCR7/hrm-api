from django.contrib import admin


class CustomAdminSite(admin.AdminSite):
    site_header = 'FlooringDeals Admin'
    site_title = 'FlooringDeals Admin'

    index_template = 'admin/custom_index.html'

    def index(self, request, extra_context=None):
        extra_context = {
            'hello': 'hello'
        }
        return super().index(request, extra_context)


admin_site = CustomAdminSite()
