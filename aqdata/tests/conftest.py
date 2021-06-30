import os
import pytest

from django.conf import settings
from django.core.management import call_command
from django.test import Client

from aqdata.models import SensorData
from aqdata.helpers import load_json_from_file


# This is the time we can use with `freezegun` for testing with the `sensor_data_set`
FREEZE_TIME = '2021-06-21T14:16:21.421Z'

# Data to use to create new `SensorData` entries
SD_TEST_DATA = {
    'esp8266id': 14907210,
    'software_version': "NRZ-2020-133",
    'BME280_humidity_pc': 50.37,
    'BME280_pressure_hpa': 1011.1406,
    'BME280_temperature_deg_c': 18.5,
    'interval': 145000,
    'max_micro': 20053,
    'min_micro': 29,
    'samples_per_sec': 4855045,
    'SDS_P2_ppm': 2.83,
    'signal_dbm': -80
}


@pytest.fixture
def client():
    '''
    Fixture to return django test client
    '''
    return Client()


@pytest.fixture
def sensor_data():
    '''
    Fixture to create a single `SensorData` db entry
    '''
    entry = SensorData.objects.create(**SD_TEST_DATA)

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
