import json
import os
import pytest

from django.conf import settings

from freezegun import freeze_time

from aqdata import helpers


@pytest.mark.django_db
@freeze_time("2021-06-21T14:16:21.421Z")
# class GetDataGradientTests:
#     '''
#     Tests for the `get_data_gradient` helper function
#     '''
#     # Filtering by `BME280_humidity_pc` returns an hours worth of valid data
#     # Filtering by `BME280_pressure_hpa` returns an empty query
#     fixtures = ['./doc/get_data_gradient_tests.json']

#     def test_function_with_valid_data(self):
#         '''
#         `get_data_gradient` should calculate the first order line of best fit over an hours worth
#         of `BME280_humidity_pc` data, and return the `m` component of the resulting `mx + c`
#         calculated by `numpy.polyfit`
#         '''
#         result = helpers.get_data_gradient('BME280_humidity_pc')

#         self.assertEqual(result, -0.10612173913043632)

#     def test_function_with_empty_queryset(self):
#         '''
#         `get_data_gradient` should return 0.000 if `SensorData` filtered over the last hour returns
#         an empty queryset
#         A first order line of best fit cannot be calculated with no data
#         '''
#         result = helpers.get_data_gradient('BME280_humidity_pc')

#         self.assertEqual(result, 0.00)

#     def test_function_with_queryset_containing_one_entry(self):
#         '''
#         `get_data_gradient` should return 0.000 if `SensorData` filtered over the last hour returns
#         a queryset containing just one entry
#         A first order line of best fit cannot be calculated with a single data point
#         '''
#         result = helpers.get_data_gradient('BME280_humidity_pc')

#         self.assertEqual(result, 0.00)

#     def test_function_with_queryset_containing_none(self):
#         '''
#         `get_data_gradient` should return 0.000 if `SensorData` filtered over the last hour returns
#         a queryset containing `None` values
#         A first order line of best fit cannot be calculated if data points contain `None`
#         '''
#         result = helpers.get_data_gradient('SDS_P1_ppm')

#         self.assertEqual(result, 0.00)


@pytest.mark.django_db
class TestGetTrend:
    '''
    Tests for the `get_trend` helper function
    '''
    def test_value_positive_returns_rising(self):  #pylint:disable=no-self-use
        '''
        An input value of 0.011 should return 1 (rising)
        '''
        assert helpers.get_trend(0.011) == 1

    def test_value_positive_returns_flat(self):  #pylint:disable=no-self-use
        '''
        An input value of 0.010 should return 0 (flat)
        '''
        assert helpers.get_trend(0.010) == 0

    def test_value_0_returns_flat(self):  #pylint:disable=no-self-use
        '''
        An input value of 0.000 should return 0 (flat)
        '''
        assert helpers.get_trend(0.000) == 0

    def test_value_negative_returns_flat(self):  #pylint:disable=no-self-use
        '''
        An input value of -0.010 should return 0 (flat)
        '''
        assert helpers.get_trend(-0.010) == 0

    def test_value_negative_returns_falling(self):  #pylint:disable=no-self-use
        '''
        An input value of -0.011 should return -1 (falling)
        '''
        assert helpers.get_trend(-0.011) == -1


@pytest.mark.django_db
class TestPreprocessUploadedJson:  #pylint:disable=too-few-public-methods
    '''
    Tests for the `preprocess_uploaded_json` helper function
    '''
    def test_preprocess_valid_json(self, upload_data):  #pylint:disable=no-self-use
        '''
        Function should output reformatted json in the correct structure if the input json data is
        valid
        '''
        doc_path = os.path.join(settings.BASE_DIR, 'doc')

        processed_json = helpers.preprocess_uploaded_json(upload_data)

        # Grab expected processed json data from doc file
        with open(os.path.join(doc_path, 'sensor_data.json')) as f:  # pylint:disable=invalid-name
            expected_json = json.load(f)

        assert processed_json == expected_json
