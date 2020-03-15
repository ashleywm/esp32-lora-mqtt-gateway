from src.mqtt_sender import MqttMessage
from pyb import RTC

sources = [
    {
        'location': 'OUTSIDE',
        'topic': '/outside/sensor/bme280',
        'payload_mapping': ['temperature', 'pressure', 'humidity']
    }
]


def parse_string_to_int(s):
    try:
        value = int(s)
    except ValueError:
        value = s + ' value is not an integer'
    return value


def transfrom_payload(payload):
    payload = payload.split(',')

    if len(payload) < 2:
        print('Payload cannot be jsonified')
        return

    source = payload[0]
    source = parse_string_to_int(source)
    del payload[0]

    source_map = sources[source]
    payload_map = source_map['payload_mapping']

    if source_map is None:
        print('Source map could not be identified for source indentifier ', source)
        return

    message_content = {
        'location': source_map['location']
    }

    for index, item in enumerate(payload_map):
        message_content[item] = payload[index]

    print(message_content)
    return MqttMessage(source_map['topic'], message_content)
