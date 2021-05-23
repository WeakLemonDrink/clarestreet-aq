import json

from django.test import TestCase
from django.urls import reverse

from rest_framework import status

from upload.models import SensorData
from upload.tests.utils import load_test_json_data


class UploadViewTests(TestCase):
    '''
    `TestCase` class for the `upload` view
    '''
    def setUp(self):
        '''
        Common setup
        '''
        self.upload_data = load_test_json_data('upload_data.json')
        self.request_url = reverse('upload')

    def test_upload_valid_data_post_returns_http_201_created(self):
        '''
        `upload` view should create a new `SensorData` entry if supplied with valid json data

        If data is valid and entry is created, HTTP_201_CREATED reponse status code should be
        returned
        '''
        response = self.client.post(
            self.request_url, json.dumps(self.upload_data), content_type="application/json"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_upload_valid_data_post_creates_new_entry(self):
        '''
        `upload` view should create a new `SensorData` entry if supplied with valid json data

        If data is valid and sent via post request, new `SensorData` entry is created
        '''
        self.client.post(
            self.request_url, json.dumps(self.upload_data), content_type="application/json"
        )

        # New `SensorData` entry should exist in the db
        self.assertTrue(SensorData.objects.all().exists())

    def test_upload_invalid_data_post_returns_http_400_bad_request(self):
        '''
        `upload` view should create a new `SensorData` entry if supplied with valid json data

        If data is invalid, HTTP_400_BAD_REQUEST reponse status code should be returned
        '''
        # Modify the upload data to remove a required field
        self.upload_data.pop('esp8266id')

        response = self.client.post(
            self.request_url, json.dumps(self.upload_data), content_type="application/json"
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_upload_invalid_data_post_doesnt_create_new_entry(self):
        '''
        `upload` view should create a new `SensorData` entry if supplied with valid json data

        If data is invalid, new `SensorData` entry should not be created
        '''
        # Modify the upload data to remove a required field
        self.upload_data.pop('esp8266id')

        self.client.post(
            self.request_url, json.dumps(self.upload_data), content_type="application/json"
        )

        # `SensorData` db should be empty
        self.assertFalse(SensorData.objects.all().exists())

    def test_post_get_rejected(self):
        '''
        `upload` view should create a new `SensorData` entry if supplied with valid json data

        If view receives a get request, request should be rejected and HTTP_405_METHOD_NOT_ALLOWED
        status returned
        '''
        response = self.client.get(self.request_url)

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
