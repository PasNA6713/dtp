from django_filters import rest_framework as filters
from django.db.models import Q

from .models import Dtp


def get_time_group(queryset, name, number):
    if number==3:
        start_time = 21
        end_time = 2
        return queryset.filter(Q(datetime__hour__gte=start_time) | Q(datetime__hour__lt=end_time))
    elif number==0:
        start_time = 2
        end_time = 11
    elif number==1:
        start_time = 11
        end_time = 16
    elif number==2:
        start_time = 16
        end_time = 21
    return queryset.filter(Q(datetime__hour__gte=start_time) & Q(datetime__hour__lt=end_time))


class DtpFilter(filters.FilterSet):
    datetime = filters.IsoDateTimeFromToRangeFilter(field_name='datetime')
    weather = filters.CharFilter(lookup_expr='icontains')
    nearby = filters.CharFilter(lookup_expr='icontains')
    road_conditions = filters.CharFilter(lookup_expr='icontains')
    
    time_group = filters.NumberFilter(method=get_time_group)

    class Meta:
        model = Dtp
        fields = "__all__"