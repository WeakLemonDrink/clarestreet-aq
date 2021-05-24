# Defines how uploaded json fields map to `SensorData` model fields
UPLOADED_JSON_FIELD_MAP = {
    'BME280_humidity': 'BME280_humidity_pc',
    'BME280_pressure': 'BME280_pressure_hpa',
    'BME280_temperature': 'BME280_temperature_deg_c',
    'interval': 'interval',
    'max_micro': 'max_micro',
    'min_micro': 'min_micro',
    'samples': 'samples_per_sec',
    'SDS_P1': 'SDS_P1_ppm',
    'SDS_P2': 'SDS_P2_ppm',
    'signal': 'signal_dbm',
}


def preprocess_uploaded_json(request_data):
    '''
    Function takes input `request_data` and outputs refactored dict to suit a
    default `SensorData` model serializer
    '''
    sensordatavalues = request_data.pop('sensordatavalues', None)

    if sensordatavalues:
        for value_pair in sensordatavalues:
            # Find the mapped field name and add to the dict if it exists
            field_name = UPLOADED_JSON_FIELD_MAP.get(value_pair['value_type'], None)

            if field_name:
                request_data[field_name] = value_pair['value']

    return request_data
