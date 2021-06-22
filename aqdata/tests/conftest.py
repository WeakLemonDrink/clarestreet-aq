import json
import os
import pytest

from django.conf import settings
from django.test import Client






@pytest.fixture
def client():
    '''
    Returns django test client
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
def upload_data():
    '''
    Returns representative upload data
    '''
    return load_test_json_data('upload_data.json')
