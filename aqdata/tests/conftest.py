import json
import os
import pytest

from django.conf import settings
from django.core.management import call_command
from django.test import Client

from aqdata.models import SensorData


# This is the time we can use with `freezegun` for testing with the `sensor_data_set`
FREEZE_TIME = '2021-06-21T14:16:21.421Z'


@pytest.fixture
def client():
    '''
    Fixture to return django test client
    '''
    return Client()


def load_test_json_data(file):
    '''
    Method loads json data from file and returns
    '''
    upload_data_file_path = os.path.join(settings.BASE_DIR, 'doc', file)

    # Load the json from file
    with open(upload_data_file_path) as f: # pylint:disable=invalid-name
        return json.load(f)


@pytest.fixture
def sensor_data():
    '''
    Fixture to create a single `SensorData` db entry
    '''
    entry = SensorData.objects.create(
        esp8266id=14907210,
        software_version="NRZ-2020-133",
        BME280_humidity_pc=50.37,
        BME280_pressure_hpa=1011.1406,
        BME280_temperature_deg_c=18.5,
        interval=145000,
        max_micro=20053,
        min_micro=29,
        samples_per_sec=4855045,
        SDS_P2_ppm=2.83,
        signal_dbm=-80
    )

    return entry


@pytest.fixture
def sensor_data_set():
    '''
    Fixture to create a set of `SensorData` db entries and return the resulting queryset
    '''
    call_command('loaddata', os.path.join(settings.BASE_DIR, 'doc', 'sensor_data_set.json'))

    return SensorData.objects.all()


@pytest.fixture
def upload_data():
    '''
    Fixture to return representative upload data
    '''
    return load_test_json_data('upload_data.json')
