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
    
    #################################################################################
    # Admin
    
    path('admin/', admin.site.urls),
    path('api/admin/user/', include('users.admin.urls')),
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
    #################################################################################
]
