# Generated by Django 3.2.3 on 2021-05-20 21:32

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SensorData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('esp8266id', models.IntegerField()),
                ('software_version', models.CharField(max_length=140)),
                ('upload_time', models.DateTimeField(auto_now_add=True)),
                ('BME280_humidity_pc', models.FloatField(blank=True, null=True)),
                ('BME280_pressure_hpa', models.FloatField(blank=True, null=True)),
                ('BME280_temperature_deg_c', models.FloatField(blank=True, null=True)),
                ('interval', models.IntegerField(blank=True, null=True)),
                ('max_micro', models.IntegerField(blank=True, null=True)),
                ('min_micro', models.IntegerField(blank=True, null=True)),
                ('samples_per_sec', models.IntegerField(blank=True, null=True)),
                ('SDS_P1_ppm', models.FloatField(blank=True, null=True)),
                ('SDS_P2_ppm', models.FloatField(blank=True, null=True)),
                ('signal_dbm', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'ordering': ['upload_time'],
            },
        ),
    ]