import json


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


def preprocess_uploaded_json(uploaded_json):
    '''
    Function takes input `uploaded_json` and outputs refactored json to suit a
    default `SensorData` model serializer
    '''

    # Convert to dict
    uploaded_dict = json.load(uploaded_json)

    sensordatavalues = uploaded_dict.pop('sensordatavalues', None)

    if sensordatavalues:
        for value_pair in sensordatavalues:
            # Find the mapped field name and add to the dict if it exists
            field_name = UPLOADED_JSON_FIELD_MAP.get(value_pair['value_type'], None)

            if field_name:
                uploaded_dict[field_name] = value_pair['value']

    return json.dumps(uploaded_dict)
