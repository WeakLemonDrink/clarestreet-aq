from rest_framework import serializers

from upload import models


class SensorDataSerializer(serializers.ModelSerializer):
    '''
    `ModelSerializer` class for the `SensorData` model
    '''

    class Meta:
        fields = ['esp8266id', 'software_version', 'upload_time',
                  'BME280_humidity_pc', 'BME280_pressure_hpa',
                  'BME280_temperature_deg_c', 'interval', 'max_micro', 'min_micro',
                  'samples_per_sec', 'SDS_P1_ppm', 'SDS_P2_ppm', 'signal_dbm']
        read_only_fields = ['upload_time']
        model = models.SensorData
