from django.urls import path
from .views import (
    Dashboard,
    ProjectsByTime,
    StaffByTime,
    CustomerByTime
)


urlpatterns = [
    path('', Dashboard.as_view(), name='dashboard-count-total'),
    path('project-by-time/', ProjectsByTime.as_view(), name='dashboard-project'),
    path('staff-by-time/', StaffByTime.as_view(), name='dashboard-staff'),
    path('customer-by-time/', CustomerByTime.as_view(), name='dashboard-customer'),
]
