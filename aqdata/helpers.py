import datetime

from django.utils import timezone

import numpy as np

from aqdata.models import SensorData


# Defines how uploaded json fields map to `SensorData` model fields
UPLOADED_JSON_FIELD_MAP = {
    'BME280_humidity': 'BME280_humidity_pc',
    'BME280_pressure': 'BME280_pressure_hpa',
    'BME280_temperature': 'BME280_temperature_deg_c',
    'interval': 'interval',
    'max_micro': 'max_micro',
    'min_micro': 'min_micro',
    'samples': 'samples_per_sec',
    'SDS_P1': 'SDS_P1_ppm',
    'SDS_P2': 'SDS_P2_ppm',
    'signal': 'signal_dbm',
}


def get_data_gradient(field):
    '''
    Function takes input `field` and calculates first order polynomial across an hours worth of
    `sensordata.field` data using `numpy.polyfit`
    Returns the `m` component of the resulting `mx + c` returned by `numpy.polyfit`
    '''
    # Return `0.000` by default
    m = 0.000  # pylint:disable=invalid-name

    an_hour_ago = timezone.now() - datetime.timedelta(hours=1)

    # Grab the last hours worth of `sensordata`
    qs = SensorData.objects.filter(upload_time__gte=an_hour_ago)

    if qs.exists() and qs.count() > 1:
        # Return the `field` values from this queryset
        data = qs.values_list(field, flat=True)

        # Make sure there are no `None` values in the data
        if None not in data:
            # Fit the data to a first order polynomial and return the `m` component
            m, _ = np.polyfit(np.arange(0, len(data)), np.array(data), 1)  # pylint:disable=invalid-name

    return m

def get_trend(gradient):
    '''
    Returns
     * 1 (rising) if `gradient` is > `upper_threshold`
     * 0 (flat) if `lower_threshold` <= `gradient` <= `upper_threshold`
     * -1 (falling) if `gradient` is < `lower_threshold`
    '''

    upper_threshold = 0.01
    lower_threshold = -0.01

    if gradient > upper_threshold:
        value = 1
    elif lower_threshold <= gradient <= upper_threshold:
        value = 0
    else:
        value = -1

    return value


def preprocess_uploaded_json(request_data):
    '''
    Function takes input `request_data` and outputs refactored dict to suit a
    default `SensorData` model serializer
    '''
    sensordatavalues = request_data.pop('sensordatavalues', None)

    if sensordatavalues:
        for value_pair in sensordatavalues:
            # Find the mapped field name and add to the dict if it exists
            field_name = UPLOADED_JSON_FIELD_MAP.get(value_pair['value_type'], None)

            if field_name:
                request_data[field_name] = value_pair['value']

    # Convert incoming pressure in Pa to hPa
    if request_data['BME280_pressure_hpa']:
        pressure_pa = float(request_data['BME280_pressure_hpa'])
        request_data['BME280_pressure_hpa'] = str(pressure_pa * (10**-2))

    return request_data
