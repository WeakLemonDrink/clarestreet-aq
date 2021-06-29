import datetime
import json
import os
import pytest

from django.conf import settings
from django.utils import timezone

from freezegun import freeze_time

from aqdata import helpers
from aqdata.models import SensorData
from aqdata.tests.conftest import FREEZE_TIME


@pytest.mark.django_db
class TestGetAppLastUpdateDatetime:
    '''
    Tests for the `get_app_last_update_datetime` helper function
    '''
    def test_function_with_valid_app_last_update(self):
        '''
        `get_app_last_update_datetime` should return a `datetime` object of
        `settings.APP_LAST_UPDATE` if the string is valid
        '''
        returned_obj = helpers.get_app_last_update_datetime()
        # The expected obj should be timezone aware
        expected_obj = timezone.make_aware(datetime.datetime(2021, 6, 9, 16, 0, 49))

        assert returned_obj == expected_obj

    @pytest.mark.parametrize(
        'test_input,expected',
        [
            ('', None),
            (None, None),
            ('2021-6-09 16:00 +0100', None),  # Not the correct format
        ]
    )
    def test_function_with_invalid_app_last_update(self, test_input, expected):
        '''
        `get_app_last_update_datetime` should return an empty string if the string returned by
        `settings.APP_LAST_UPDATE` is not a valid date string
        '''
        # Update `settings.APP_LAST_UPDATE` with the `test_input`
        settings.APP_LAST_UPDATE = test_input
        assert helpers.get_app_last_update_datetime() == expected


@pytest.mark.django_db
class TestGetDataGradient:
    '''
    Tests for the `get_data_gradient` helper function
    '''
    def test_function_with_empty_queryset(self):
        '''
        `get_data_gradient` should return 0.000 if `SensorData` filtered over the last hour returns
        an empty queryset
        A first order line of best fit cannot be calculated with no data
        '''
        # Confirm there's no entries in the `SensorData` db
        assert SensorData.objects.all().exists() is False

        result = helpers.get_data_gradient('BME280_humidity_pc')

        assert result == 0.00

    def test_function_with_queryset_containing_one_entry(self, sensor_data):
        '''
        `get_data_gradient` should return 0.000 if `SensorData` filtered over the last hour returns
        a queryset containing just one entry
        A first order line of best fit cannot be calculated with a single data point
        '''
        result = helpers.get_data_gradient('BME280_humidity_pc')

        assert result == 0.00

    @freeze_time(FREEZE_TIME)
    def test_function_with_queryset_containing_none(self, sensor_data_hour_set):
        '''
        `get_data_gradient` should return 0.000 if `SensorData` filtered over the last hour returns
        a queryset containing `None` values
        A first order line of best fit cannot be calculated if data points contain `None`
        '''
        # return a entry from the `sensor_data_hour_set` and update to contain a `None` value
        entry = sensor_data_hour_set.last()
        entry.SDS_P1_ppm = None
        entry.save()

        result = helpers.get_data_gradient('SDS_P1_ppm')

        assert result == 0.00

    @freeze_time(FREEZE_TIME)
    @pytest.mark.parametrize(
        'test_input,expected',
        [
            ('BME280_humidity_pc', -0.10612173913043632),
            ('BME280_pressure_hpa', 0.026518869565194374),
            ('BME280_temperature_deg_c', 0.035091304347826056),
            ('SDS_P1_ppm', 0.038843478260869424),
            ('SDS_P2_ppm', 0.012034782608695602),
        ]
    )
    def test_function_with_valid_data(self, sensor_data_hour_set, test_input, expected):
        '''
        `get_data_gradient` should calculate the first order line of best fit over an hours worth
        of `test_input` data, and return the `m` component of the resulting `mx + c`
        calculated by `numpy.polyfit`
        '''
        # Confirm some data exists in the db
        assert SensorData.objects.all().exists() is True
        result = helpers.get_data_gradient(test_input)

        assert result == expected


class TestGetTrend:
    '''
    Tests for the `get_trend` helper function
    '''
    @pytest.mark.parametrize(
        'test_input,expected',
        [
            (0.011, 1),  # An input value of 0.011 should return 1 (rising)
            (0.010, 0),  # An input value of 0.010 should return 0 (flat)
            (0.000, 0),  # An input value of 0.000 should return 0 (flat)
            (-0.010, 0),  # An input value of -0.010 should return 0 (flat)
            (-0.011, -1),  # An input value of -0.011 should return -1 (falling)
        ]
    )
    def test_get_trend(self, test_input, expected):
        '''
        `get_trend` should return either `1`, `0` or `-1` to show whether the input gradient is
        rising, flat or falling
        '''
        assert helpers.get_trend(test_input) == expected


class TestPreprocessUploadedJson:
    '''
    Tests for the `preprocess_uploaded_json` helper function
    '''
    def test_preprocess_uploaded_json(self, upload_data):
        '''
        `preprocess_uploaded_json` function should output reformatted json in the correct
        structure if the input json data is valid
        '''
        doc_path = os.path.join(settings.BASE_DIR, 'doc')

        processed_json = helpers.preprocess_uploaded_json(upload_data)

        # Grab expected processed json data from doc file
        with open(os.path.join(doc_path, 'sensor_data.json')) as f:  # pylint:disable=invalid-name
            expected_json = json.load(f)

        assert processed_json == expected_json
