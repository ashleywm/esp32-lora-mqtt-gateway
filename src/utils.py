from src.mqtt_sender import MqttMessage
import ujson

locations = [
    {
        'id': 1,
        'name': 'allotment'
    }
]

sensors = [
    {
        'id': 1,
        'name': 'bme280',
        'payload_mapping': ['temperature', 'pressure', 'humidity']
    },
    {
        'id': 2,
        'name': 'bh1750',
        'payload_mapping': ['luminosity']
    },
    {
        'id': 3,
        'name': 'ds18b20',
        'payload_mapping': ['temperature']
    },
    {
        'id': 4,
        'name': 'csms',
        'payload_mapping': ['mositure']
    },
    {
        'id': 5,
        'name': 'battery',
        'payload_mapping': ['battery_level']
    }
]


def parse_string_to_int(s):
    try:
        value = int(s)
    except ValueError:
        value = s + ' value is not an integer'
    return value


def parse_string_to_float(s):
    try:
        value = float(s)
    except ValueError:
        value = s + ' value is not an integer'
    return value


def represents_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


def represents_float(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def transfrom_payload(payload):
    payload = payload.split(',')

    if len(payload) < 3:
        print('Payload cannot be jsonified')
        return

    location_id = payload[0]
    location_id = parse_string_to_int(location_id)

    sensor_id = payload[1]
    sensor_id = parse_string_to_int(sensor_id)

    del payload[0]
    del payload[0]

    location = None
    sensor = None

    for loc in locations:
        if loc['id'] == location_id:
            location = loc

    for sen in sensors:
        if sen['id'] == sensor_id:
            sensor = sen

    payload_map = sensor['payload_mapping']

    message_content = {}

    for index, item in enumerate(payload_map):
        reading = payload[index]
        if represents_int(reading):
            message_content[item] = parse_string_to_int(reading)
        elif represents_float(reading):
            message_content[item] = parse_string_to_float(reading)
        else:
            message_content[item] = reading

    topic = ''

    if location['name']:
        topic += '/' + location['name']
    else:
        topic += '/unknown'

    if sensor['name']:
        topic += '/sensor/' + sensor['name']
    else:
        topic += '/sensor/unkown'

    message_content = ujson.dumps(message_content)

    return MqttMessage(topic, message_content)
