from django_filters import rest_framework as filters

from aqdata.models import SensorData


class SensorDataFilter(filters.FilterSet):
    '''
    Defines a `FilterSet` for the `SensorData` model
    '''
    upload_time = filters.IsoDateTimeFromToRangeFilter()

    class Meta:
        fields = ['upload_time']
        model = SensorData
