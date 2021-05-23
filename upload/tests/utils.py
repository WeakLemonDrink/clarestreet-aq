import os
import json

from django.conf import settings

def load_test_json_data(file):
    '''
    Method loads json data from file and returns
    '''
    upload_data_file_path = os.path.join(settings.BASE_DIR, 'doc', file)

    # Load the json from file
    with open(upload_data_file_path) as f: # pylint:disable=invalid-name
        return json.load(f)
