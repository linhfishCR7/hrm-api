import django_filters
from django_filters.rest_framework import filters
import django_filters

from base.utils import print_value

class SalaryFilter(django_filters.FilterSet):
    month = django_filters.CharFilter(method="filter_month")
    year = django_filters.CharFilter(method="filter_year")
    staff = django_filters.CharFilter(method="filter_staff")

    def filter_month(self, queryset, name, value):
        return queryset.filter(date__month=value)
    
    def filter_year(self, queryset, name, value):
        return queryset.filter(date__year=value)
    
    def filter_staff(self, queryset, name, value):
        return queryset.filter(staff=value)

    
