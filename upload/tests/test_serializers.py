from django.test import TestCase

from upload.models import SensorData
from upload.serializers import SensorDataSerializer
from upload.tests.utils import load_test_json_data


class SensorDataSerializerTests(TestCase):
    '''
    `TestCase` class for the `SensorDataSerializer` model serializer
    '''
    def setUp(self):
        '''
        Common setup
        '''
        # Load the json from file
        self.upload_data = load_test_json_data('upload_data.json')

    def test_deserializer_is_valid_true(self):
        '''
        `SensorDataSerializer` model serializer should create a new `SensorData`
        model entry if valid json data is supplied

        `./doc/upload_data.json` is valid json data for the `SensorData` model

        `SensorDataSerializer` `is_valid()` should return `True` if supplied
        with valid json data to deserialize
        '''
        serializer = SensorDataSerializer(data=self.upload_data)

        self.assertTrue(serializer.is_valid())

    def test_deserializer_creates_new_entry(self):
        '''
        `SensorDataSerializer` model serializer should create a new `SensorData`
        model entry if valid json data is supplied
        '''
        serializer = SensorDataSerializer(data=self.upload_data)

        # Call `is_valid` first then `save`
        serializer.is_valid()
        serializer.save()

        # `SensorData` entry should exist following `save`
        self.assertTrue(SensorData.objects.all().exists())
