import os
import pytest

from django.conf import settings
from django.core.management import call_command
from django.test import Client

from aqdata.models import SensorData
from aqdata.helpers import load_json_from_file


# This is the time we can use with `freezegun` for testing with the `sensor_data_set`
FREEZE_TIME = '2021-06-21T14:16:21.421Z'


@pytest.fixture
def client():
    '''
    Fixture to return django test client
    '''
    return Client()


@pytest.fixture
def sensor_data():
    '''
    Fixture to return representative a serialized `SensorData` entry
    '''
    return load_json_from_file(os.path.join(settings.BASE_DIR, 'doc', 'sensor_data.json'))


@pytest.fixture
def sensor_data_entry(sensor_data):
    '''
    Fixture to create a single `SensorData` db entry
    '''
    entry = SensorData.objects.create(**sensor_data)

    return entry


@pytest.fixture
def sensor_data_day_set():
    '''
    Fixture to create a set of a days worth of `SensorData` db entries and return the resulting
    queryset
    '''
    call_command('loaddata', os.path.join(settings.BASE_DIR, 'doc', 'sensor_data_day.json'))

    return SensorData.objects.all()


@pytest.fixture
def sensor_data_hour_set():
    '''
    Fixture to create a set of an hours worth of `SensorData` db entries and return the resulting
    queryset
    '''
    call_command('loaddata', os.path.join(settings.BASE_DIR, 'doc', 'sensor_data_hour.json'))

    return SensorData.objects.all()


@pytest.fixture
def upload_data():
    '''
    Fixture to return representative upload data
    '''
    return load_json_from_file(os.path.join(settings.BASE_DIR, 'doc', 'upload_data.json'))
