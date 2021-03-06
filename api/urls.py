"""api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # COMMON API METHODS.
    path('api/common/', include('base.urls'), name='common'),
    # Auth
    path('api/auth/', include('users.auth.urls')),
    #################################################################################
    # User
    
    path('api/user/day-off-years/', include('day_off_years.user.urls')),
    path('api/user/day-off-year-details/', include('day_off_year_details.user.urls')),
    path('api/user/day-off-types/', include('day_off_types.user.urls')),
    path('api/user/notification/', include('notification.user.urls')),
    path('api/user/salary/', include('salaries.user.urls')),
    path('api/user/employment-contract/', include('employment_contracts.user.urls')),
    path('api/user/staffs/', include('staffs.user.urls')),
    path('api/user/dashboard/', include('dashboard.user.urls')),

    #################################################################################
    # Admin
    
    path('admin/', admin.site.urls),
    path('api/admin/user/', include('users.admin.urls')),
    path('api/admin/notification/', include('notification.admin.urls')),
    path('api/admin/companies/', include('companies.admin.urls')),
    path('api/admin/branchs/', include('branchs.admin.urls')),
    path('api/admin/dashboard/', include('dashboard.admin.urls')),

    #################################################################################

    # Hrm
    path('api/hrm/certificate-types/', include('certificate_types.hrm.urls')),
    path('api/hrm/day-off-types/', include('day_off_types.hrm.urls')),
    path('api/hrm/degree-types/', include('degree_types.hrm.urls')),
    path('api/hrm/employment-contract-types/', include('employment_contract_types.hrm.urls')),
    path('api/hrm/nationalities/', include('nationalities.hrm.urls')),
    path('api/hrm/religions/', include('religions.hrm.urls')),
    path('api/hrm/ethnicities/', include('ethnicities.hrm.urls')),
    path('api/hrm/positions/', include('positions.hrm.urls')),
    path('api/hrm/companies/', include('companies.hrm.urls')),
    path('api/hrm/kinds-of-work/', include('kinds_of_work.hrm.urls')),
    path('api/hrm/literacy/', include('literacy.hrm.urls')),
    path('api/hrm/customers/', include('customers.hrm.urls')),
    path('api/hrm/projects/', include('projects.hrm.urls')),
    path('api/hrm/branchs/', include('branchs.hrm.urls')),
    path('api/hrm/departments/', include('departments.hrm.urls')),
    path('api/hrm/staffs/', include('staffs.hrm.urls')),
    path('api/hrm/promotions/', include('promotions.hrm.urls')),
    path('api/hrm/skills/', include('skills.hrm.urls')),
    path('api/hrm/urgent-contacts/', include('urgent_contacts.hrm.urls')),
    path('api/hrm/bonuses/', include('bonuses.hrm.urls')),
    path('api/hrm/health-status/', include('health_status.hrm.urls')),
    path('api/hrm/day-off-years/', include('day_off_years.hrm.urls')),
    path('api/hrm/certificate/', include('certificate.hrm.urls')),
    path('api/hrm/degree/', include('degree.hrm.urls')),
    path('api/hrm/discipline/', include('discipline.hrm.urls')),
    path('api/hrm/salary/', include('salaries.hrm.urls')),
    path('api/hrm/timekeeping/', include('timekeeping.hrm.urls')),
    path('api/hrm/staff-project/', include('staff_project.hrm.urls')),
    path('api/hrm/employment-contract/', include('employment_contracts.hrm.urls')),
    path('api/hrm/up-salary/', include('up_salaries.hrm.urls')),
    path('api/hrm/recruitment-requirement/', include('recruitment_requirements.hrm.urls')),
    path('api/hrm/recruitment-requirement-detail/', include('recruitment_requirement_details.hrm.urls')),
    path('api/hrm/recruitment-tracking/', include('recruitment_tracking.hrm.urls')),
    path('api/hrm/trainning-requirement/', include('trainning_requirement.hrm.urls')),
    path('api/hrm/trainning-requirement-detail/', include('trainning_requirement_detail.hrm.urls')),
    path('api/hrm/dashboard/', include('dashboard.hrm.urls')),
    path('api/hrm/on-business/', include('on_business.hrm.urls')),
    path('api/hrm/notification/', include('notification.hrm.urls')),

    #################################################################################
]
