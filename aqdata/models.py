import datetime
import numpy as np

from django.db import models
from django.conf import settings


class SensorData(models.Model):
    '''
    Defines database structure for uploaded sensor data
    '''

    # Timestamp and device info
    esp8266id = models.IntegerField()
    software_version = models.CharField(max_length=140)
    upload_time = models.DateTimeField(auto_now_add=True)
    # Web app info
    app_version = models.CharField(max_length=140, blank=True, null=True)
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
    # PM 2.5 and PM 10 24 hour moving averages
    p1_ppm_24hr_moving_avg = models.FloatField(blank=True, null=True)
    p2_ppm_24hr_moving_avg = models.FloatField(blank=True, null=True)

    class Meta:
        ordering = ['upload_time']

    def save(self, *args, **kwargs):
        '''
        Override default save to automatically populate `app_version` field on initial save
        '''
        if self.pk is None:
            if settings.APP_VERSION:
                self.app_version = settings.APP_VERSION

        return super().save(*args, **kwargs)

    def update_moving_averages(self):
        '''
        Gets a queryset of the last 24hrs of data from `self.upload_time`, calculate 24 hour
        averages for `SDS_P1_ppm` and `SDS_P2_ppm` fields and save to `p1_ppm_24hr_moving_avg` and
        `p2_ppm_24hr_moving_avg` fields
        '''
        # Grab the `SensorData` entries within a 24 range
        filter_start = self.upload_time - datetime.timedelta(hours=24)
        filter_stop = self.upload_time

        sensor_data_qs = self._meta.model.objects.filter(
            upload_time__gte=filter_start, upload_time__lte=filter_stop
        )

        for target_field, avg_field in [
                ('SDS_P1_ppm', 'p1_ppm_24hr_moving_avg'), ('SDS_P2_ppm', 'p2_ppm_24hr_moving_avg')
            ]:
            # Only save average if `target_field` contains a valid value
            if getattr(self, target_field) is not None:
                target_field_array = np.array(sensor_data_qs.values_list(target_field, flat=True))
                # Strip out any `None` values from the array
                target_field_array = target_field_array[target_field_array != np.array(None)]

                # Save the mean to the avg_field
                setattr(self, avg_field, np.mean(target_field_array))

        # Save the instance
        self.save()

    def __str__(self):
        return '{!s} {}'.format(self.id, self.upload_time.strftime('%Y-%m-%d %H:%M:%S'))
