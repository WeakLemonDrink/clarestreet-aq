import json
import os

from django.conf import settings
from django.test import TestCase

from freezegun import freeze_time

from aqdata import helpers
from aqdata.tests.utils import load_test_json_data


@freeze_time("2021-06-21T14:16:21.421Z")
class GetDataGradient(TestCase):
    '''
    Tests for the `get_data_gradient` helper function
    '''

    fixtures = ['./doc/sensor_data_week.json']

    def test_function(self):
        '''
        Nlaja
        '''
        self.assertTrue(helpers.get_data_gradient('BME280_humidity_pc'))


class PreprocessUploadedJsonTests(TestCase):
    '''
    Tests for the `preprocess_uploaded_json` helper function
    '''
    def test_preprocess_valid_json(self):
        '''
        Function should output reformatted json in the correct structure if the input json data is
        valid
        '''
        doc_path = os.path.join(settings.BASE_DIR, 'doc')

        # Grab example json data from doc file
        upload_dict = load_test_json_data('upload_data.json')

        processed_json = helpers.preprocess_uploaded_json(upload_dict)

        # Grab expected processed json data from doc file
        with open(os.path.join(doc_path, 'sensor_data.json')) as f:  # pylint:disable=invalid-name
            expected_json = json.load(f)

        self.assertDictEqual(processed_json, expected_json)
