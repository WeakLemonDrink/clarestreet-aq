import json


# Defines how uploaded json fields map to `SensorData` model fields
UPLOADED_JSON_FIELD_MAP = (
    ('BME280_humidity', 'BME280_humidity_pc'),
    ('BME280_pressure', 'BME280_pressure_hpa'),
    ('BME280_temperature', 'BME280_temperature_deg_c'),
    ('interval', 'interval'),
    ('max_micro', 'max_micro'),
    ('min_micro', 'min_micro'),
    ('samples', 'samples_per_sec')
    ('SDS_P1', 'SDS_P1_ppm'),
    ('SDS_P2', 'SDS_P2_ppm'),
    ('signal', 'signal_dbm'),
)


def preprocess_uploaded_json(uploaded_json):
    '''
    Function takes input `uploaded_json` and outputs refactored json to suit a
    default `SensorData` model serializer
    '''

    # Convert to dict
    uploaded_dict = json.load(uploaded_json)

    sensordatavalues = uploaded_dict.pop('sensordatavalues', None)

    if sensordatavalues:
        # Loop through the field map and save the data to the uploaded_dict
        for json_field, model_field in UPLOADED_JSON_FIELD_MAP:
            # Check that json_field exists in the uploaded data
            if json_field in [i['value_type'] for i in sensordatavalues]:

    return refactored_json
