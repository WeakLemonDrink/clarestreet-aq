import datetime
import json
import pytest

from django.urls import reverse
from django.utils.http import urlencode

from freezegun import freeze_time
from rest_framework import status

from aqdata.models import SensorData
from aqdata.tests.conftest import FREEZE_TIME


@pytest.mark.django_db
class TestHomeView:
    '''
    Tests for the `HomeView` view
    '''
    request_url = reverse('home')

    @pytest.mark.parametrize('test_input_field', ['latest_sensor_data', 'trends'])
    def test_context_not_built_if_data_doesnt_exist(self, client, test_input_field):
        '''
        `HomeView` view should not add the test inputs as keys to the context dictionary if data
        doesn't exist in the `SensorData` db
        '''
        response = client.get(self.request_url)

        assert response.context.get(test_input_field, None) is None

    @freeze_time(FREEZE_TIME)
    @pytest.mark.parametrize(
        'test_input_field,expected',
        [
            ('BME280_humidity_pc', -1),
            ('BME280_pressure_hpa', 1),
            ('BME280_temperature_deg_c', 1),
            ('SDS_P1_ppm', 1),
            ('SDS_P2_ppm', 1),
        ]
    )
    def test_trend_data_saved_to_context(
        self, client, sensor_data_hour_set, test_input_field, expected
    ):
        '''
        `HomeView` view should add values describing the trends in the last hours worth of data
        to the context
        '''
        response = client.get(self.request_url)

        assert response.context['trends'] is not None

        # Grab the trends dictionary and check each one has a valid trend integer
        trends = response.context['trends']

        assert trends[test_input_field] == expected


@pytest.mark.django_db
class TestSensorDataViewSet:
    '''
    Tests for the `SensorDataViewSet` viewset
    '''
    request_url = reverse('sensordata-list')

    def test_upload_valid_data_post_returns_http_201_created(self, client, upload_data):
        '''
        `SensorDataViewSet` list view should create a new `SensorData` entry if supplied with
        valid json data

        If data is valid and entry is created, HTTP_201_CREATED reponse status code should be
        returned
        '''
        response = client.post(
            self.request_url, json.dumps(upload_data), content_type="application/json"
        )

        assert response.status_code == status.HTTP_201_CREATED

    def test_upload_valid_data_post_creates_new_entry(self, client, upload_data):
        '''
        `SensorDataViewSet` list view should create a new `SensorData` entry if supplied with valid
        json data

        If data is valid and sent via post request, new `SensorData` entry is created
        '''
        client.post(
            self.request_url, json.dumps(upload_data), content_type="application/json"
        )

        # New `SensorData` entry should exist in the db
        assert SensorData.objects.all().exists() is True

    def test_upload_valid_data_post_calls_sensor_data_update_moving_averages(
        self, client, upload_data
    ):
        '''
        `SensorDataViewSet` list view should create a new `SensorData` entry if supplied with valid
        json data

        If data is valid and sent via post request, new `SensorData` entry is created and
        `p1_ppm_24hr_moving_avg` and `p2_ppm_24hr_moving_avg` fields are automatically populated
        by `SensorData` `post_save` signal
        '''
        client.post(
            self.request_url, json.dumps(upload_data), content_type="application/json"
        )
        # Grab the new entry
        new_entry = SensorData.objects.all().first()

        # `SensorData` entry `p1_ppm_24hr_moving_avg` and `p2_ppm_24hr_moving_avg` fields should
        # be filled following `save`
        assert new_entry.SDS_P1_ppm is not None
        assert new_entry.SDS_P2_ppm is not None
        assert new_entry.p1_ppm_24hr_moving_avg is not None
        assert new_entry.p2_ppm_24hr_moving_avg is not None

    def test_upload_invalid_data_post_returns_http_400_bad_request(self, client, upload_data):
        '''
        `SensorDataViewSet` list view should create a new `SensorData` entry if supplied with
        valid json data

        If data is invalid, HTTP_400_BAD_REQUEST reponse status code should be returned
        '''
        # Modify the upload data to remove a required field
        upload_data.pop('esp8266id')

        response = client.post(
            self.request_url, json.dumps(upload_data), content_type="application/json"
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_upload_invalid_data_post_doesnt_create_new_entry(self, client, upload_data):
        '''
        `SensorDataViewSet` list view should create a new `SensorData` entry if supplied with
        valid json data

        If data is invalid, new `SensorData` entry should not be created
        '''
        # Modify the upload data to remove a required field
        upload_data.pop('esp8266id')

        client.post(
            self.request_url, json.dumps(upload_data), content_type="application/json"
        )

        # `SensorData` db should be empty
        assert SensorData.objects.all().exists() is False

    def test_list_view_filtering_by_upload_time(self, client, sensor_data_hour_set):
        '''
        `SensorDataViewSet` list view should return filtered `SensorData` entries if supplied with
        valid querystring parameters
        Filtering by `upload_time` allows us to return data suitable for plotting on a chart
        '''
        upload_time_before = sensor_data_hour_set.last().upload_time
        upload_time_after = upload_time_before - datetime.timedelta(minutes=30)

        response = client.get(
            self.request_url + '?' + urlencode(
                {
                    'upload_time_after': upload_time_after.isoformat(),
                    'upload_time_before': upload_time_before.isoformat()
                }
            )
        )

        # Response should contain HTTP_200_OK to confirm filter works correctly
        assert response.status_code == status.HTTP_200_OK
        # Returned items should be less than the original queryset
        assert len(json.loads(response.content)) < sensor_data_hour_set.count()
