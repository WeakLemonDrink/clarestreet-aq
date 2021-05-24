from django.db import models


class SensorData(models.Model):
    '''
    Defines database structure for uploaded sensor data
    '''

    # Timestamp and device info
    esp8266id = models.IntegerField()
    software_version = models.CharField(max_length=140)
    upload_time = models.DateTimeField(auto_now_add=True)
    # Sensor readings optional in case any value is not uploaded as part of the
    # packet
    BME280_humidity_pc = models.FloatField(blank=True, null=True)
    BME280_pressure_hpa = models.FloatField(blank=True, null=True)
    BME280_temperature_deg_c = models.FloatField(blank=True, null=True)
    interval = models.IntegerField(blank=True, null=True)
    max_micro = models.IntegerField(blank=True, null=True)
    min_micro  = models.IntegerField(blank=True, null=True)
    samples_per_sec = models.IntegerField(blank=True, null=True)
    SDS_P1_ppm = models.FloatField(blank=True, null=True)
    SDS_P2_ppm = models.FloatField(blank=True, null=True)
    signal_dbm = models.IntegerField(blank=True, null=True)

    class Meta:
        ordering = ['upload_time']
