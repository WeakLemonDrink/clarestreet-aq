import json
import os

from django.conf import settings
from django.test import TestCase

from upload import serializers


class SensorDataSerializerTests(TestCase):
    '''
    `TestCase` class for the `SensorDataSerializer` model serializer
    '''

    def test_deserializer_is_valid_true(self):
        '''
        `SensorDataSerializer` model serializer should create a new `SensorData`
        model entry if valid json data is supplied

        `./doc/example_data.json` is valid json data gathered from a esp8266
        sensor running airrohr-firmware

        `SensorDataSerializer` `is_valid()` should return `True` if supplied
        with valid json data to deserialize
        '''

        upload_data_file_path = os.path.join(settings.BASE_DIR, 'doc',
                                             'example_data.json')

        # Load the json from file
        with open(upload_data_file_path) as f: # pylint:disable=invalid-name
            upload_data = json.load(f)

        serializer = serializers.SensorDataSerializer(data=upload_data)

        self.assertTrue(serializer.is_valid())
