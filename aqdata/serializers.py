from rest_framework import serializers

from aqdata.models import SensorData


class SensorDataSerializer(serializers.ModelSerializer):
    '''
    `ModelSerializer` class for the `SensorData` model
    '''

    class Meta:
        fields = [
            'esp8266id', 'software_version', 'upload_time', 'BME280_humidity_pc',
            'BME280_pressure_hpa', 'BME280_temperature_deg_c', 'interval', 'max_micro',
            'min_micro', 'samples_per_sec', 'SDS_P1_ppm', 'SDS_P2_ppm', 'signal_dbm',
            'p1_ppm_24hr_moving_avg', 'p2_ppm_24hr_moving_avg'
        ]
        read_only_fields = [
            'upload_time', 'p1_ppm_24hr_moving_avg', 'p2_ppm_24hr_moving_avg'
        ]
        model = SensorData
