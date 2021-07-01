from django.conf import settings

import pytest

from aqdata.models import SensorData


@pytest.mark.django_db
class TestSensorDataModel:
    '''
    Tests for the `SensorData` model
    '''
    def test_model_save_method_updates_app_version_if_valid(self, sensor_data_entry):
        '''
        `SensorData` model `save()` method should update the `app_version` field with
        `settings.APP_VERSION` on initial save if the version string is valid
        '''
        assert sensor_data_entry.app_version == settings.APP_VERSION

    @pytest.mark.parametrize(
        'test_input', [None, '']
    )
    def test_model_save_method_doesnt_update_app_version_if_invalid(self, test_input, sensor_data):
        '''
        `SensorData` model `save()` method should not update the `app_version` field on initial
        save if the `settings.APP_VERSION` string is invalid or missing
        '''
        # Update the settings
        settings.APP_VERSION = test_input

        # Make a `SensorData` entry now the settings have been updated
        sensor_data_entry = SensorData.objects.create(**sensor_data)

        # `app_version` should be empty
        assert sensor_data_entry.app_version is None

    def test_model_str_method_returns_correct_string(self, sensor_data_entry):
        '''
        `SensorData` model `str()` method should return a string in the format:
          <id> <timestamp.isoformat()>
        '''
        expected_str = '{!s} {}'.format(
          sensor_data_entry.id,
          sensor_data_entry.upload_time.strftime('%Y-%m-%d %H:%M:%S')
        )

        assert str(sensor_data_entry) == expected_str

    @pytest.mark.parametrize(
            'test_input_field,expected', [
                ('p1_ppm_24hr_moving_avg', 9.352899824253075),
                ('p2_ppm_24hr_moving_avg', 6.711810193321617)
            ]
        )
    def test_update_moving_averages_updates_moving_avg_fields(
        self, sensor_data_day_set, test_input_field, expected
    ):
        '''
        `SensorData` model `update_moving_averages` function should update the instance
        `p1_ppm_24hr_moving_avg` and `p2_ppm_24hr_moving_avg` fields if `SDS_P1_ppm` and
        `SDS_P2_ppm` fields are filled
        '''
        # Get the last entry in the poplulated `SensorData` db
        sensor_data_entry = SensorData.objects.latest('upload_time')
        # Call `update_moving_averages()`
        sensor_data_entry.update_moving_averages()

        assert getattr(sensor_data_entry, test_input_field) == expected

    def test_update_moving_averages_doesnt_update_moving_avg_fields_if_target_field_none(
        self, sensor_data_day_set
    ):
        '''
        `SensorData` model `update_moving_averages` function should not update the instance
        `p1_ppm_24hr_moving_avg` field if `SDS_P1_ppm` is not filled
        '''
        # Get the last entry in the poplulated `SensorData` db
        sensor_data_entry = SensorData.objects.latest('upload_time')
        # Update the entry to make field `None` and call function
        sensor_data_entry.SDS_P1_ppm = None
        sensor_data_entry.update_moving_averages()

        assert sensor_data_entry.p1_ppm_24hr_moving_avg is None
