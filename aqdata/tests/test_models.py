from django.conf import settings

import pytest

from aqdata.models import SensorData
from aqdata.tests.conftest import SD_TEST_DATA


@pytest.mark.django_db
class TestSensorDataModel:
    '''
    Tests for the `SensorData` model
    '''
    def test_model_save_method_updates_app_version_if_valid(self, sensor_data):
        '''
        `SensorData` model `save()` method should update the `app_version` field with
        `settings.APP_VERSION` on initial save if the version string is valid
        '''
        assert sensor_data.app_version == settings.APP_VERSION

    @pytest.mark.parametrize(
        'test_input', [None, '']
    )
    def test_model_save_method_doesnt_update_app_version_if_invalid(self, test_input):
        '''
        `SensorData` model `save()` method should not update the `app_version` field on initial
        save if the `settings.APP_VERSION` string is invalid or missing
        '''
        # Update the settings
        settings.APP_VERSION = test_input

        # Make a `SensorData` entry now the settings have been updated
        sensor_data = SensorData.objects.create(**SD_TEST_DATA)

        # `app_version` should be empty
        assert sensor_data.app_version is None

    def test_model_str_method_returns_correct_string(self, sensor_data):
        '''
        `SensorData` model `str()` method should return a string in the format:
          <id> <timestamp.isoformat()>
        '''
        expected_str = '{!s} {}'.format(
          sensor_data.id,
          sensor_data.upload_time.strftime('%Y-%m-%d %H:%M:%S')
        )

        assert str(sensor_data) == expected_str
