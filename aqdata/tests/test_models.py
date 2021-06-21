from django.test import TestCase

from aqdata.models import SensorData


class SensorDataModelTests(TestCase):
    '''
    `TestCase` class for the `SensorData` model
    '''
    def test_model_str_method_returns_correct_string(self):
        '''
        `SensorData` model `str()` method should return a string in the format:
          <id> <timestamp.isoformat()>
        '''
        # Make a `SensorData` entry
        entry = SensorData.objects.create(esp8266id=14907210, software_version='NRZ-2020-133')

        expected_str = '{!s} {}'.format(entry.id, entry.upload_time.strftime('%Y-%m-%d %H:%M:%S'))

        self.assertEqual(str(entry), expected_str)
