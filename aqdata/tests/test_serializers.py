import pytest

from aqdata.models import SensorData
from aqdata.serializers import SensorDataSerializer


@pytest.mark.django_db
class TestSensorDataSerializer:
    '''
    Tests for the `SensorDataSerializer` model serializer
    '''
    def test_deserializer_is_valid_true(self, upload_data):
        '''
        `SensorDataSerializer` model serializer should create a new `SensorData`
        model entry if valid json data is supplied

        `./doc/upload_data.json` is valid json data for the `SensorData` model

        `SensorDataSerializer` `is_valid()` should return `True` if supplied
        with valid json data to deserialize
        '''
        serializer = SensorDataSerializer(data=upload_data)

        assert serializer.is_valid() is True

    def test_deserializer_creates_new_entry(self, upload_data):
        '''
        `SensorDataSerializer` model serializer should create a new `SensorData`
        model entry if valid json data is supplied
        '''
        serializer = SensorDataSerializer(data=upload_data)

        # Call `is_valid` first then `save`
        serializer.is_valid()
        serializer.save()

        # `SensorData` entry should exist following `save`
        assert SensorData.objects.all().exists() is True
