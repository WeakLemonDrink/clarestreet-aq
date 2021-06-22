import pytest


@pytest.mark.django_db
class TestSensorDataModel:
    '''
    Tests for the `SensorData` model
    '''
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
