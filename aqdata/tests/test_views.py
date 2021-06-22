import json
import pytest

from django.urls import reverse

from rest_framework import status

from aqdata.models import SensorData


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
