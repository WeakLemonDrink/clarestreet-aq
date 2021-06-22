import pytest

from aqdata.models import SensorData


@pytest.mark.django_db
class TestSensorDataModel:  #pylint:disable=too-few-public-methods
    '''
    `TestCase` class for the `SensorData` model
    '''
    def test_model_str_method_returns_correct_string(self):  #pylint:disable=no-self-use
        '''
        `SensorData` model `str()` method should return a string in the format:
          <id> <timestamp.isoformat()>
        '''
        # Make a `SensorData` entry
        entry = SensorData.objects.create(esp8266id=14907210, software_version='NRZ-2020-133')

        expected_str = '{!s} {}'.format(entry.id, entry.upload_time.strftime('%Y-%m-%d %H:%M:%S'))

        assert str(entry) == expected_str
