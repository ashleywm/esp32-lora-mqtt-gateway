import ujson
import mappings
import usocket


def is_connected():
    try:
        s = usocket.socket(usocket.AF_INET, usocket.SOCK_RAW, 1)
        addr = usocket.getaddrinfo('192.168.32.1', 1)[0][-1][0]  # ip address
        s.connect((addr, 1))
        s.close()
        return True
    except Exception as e:
        print(e)
        pass
    return False


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


def transform_rssi_payload(rssi):
    topic = '/allotment/sensor/sx1276'
    message_content = {}

    if represents_int(rssi):
        message_content["rssi"] = parse_string_to_int(rssi)
    elif represents_float(rssi):
        message_content["rssi"] = parse_string_to_float(rssi)
    else:
        message_content["rssi"] = rssi

    message_content = ujson.dumps(message_content)

    return (topic, message_content)


def transfrom_payload(payload):
    payload = payload.split(',')

    if len(payload) < 3:
        print('Payload cannot be jsonified')
        return (None, None)

    location_id = payload[0]
    location_id = parse_string_to_int(location_id)

    sensor_id = payload[1]
    sensor_id = parse_string_to_int(sensor_id)

    del payload[0]
    del payload[0]

    location = None
    sensor = None

    for loc in mappings.locations:
        if loc['id'] == location_id:
            location = loc

    for sen in mappings.sensors:
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

    return (topic, message_content)
