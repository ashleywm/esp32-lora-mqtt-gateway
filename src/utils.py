from src.mqtt_sender import MqttMessage
import ujson 

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

def isfloat(value):
  try:
    float(value)
    return True
  except ValueError:
    return False

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

    message_content = {}

    for index, item in enumerate(payload_map):
        value = payload[index]

        if isfloat(value):
            value = float(value)

        message_content[item] = value

    message_content = ujson.dumps(message_content)

    return MqttMessage(source_map['topic'], message_content)
