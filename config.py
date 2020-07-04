lora_settings = {
    'frequency': 433E6,
    'frequency_offset': 0,
    'tx_power_level': 14,
    'signal_bandwidth': 125E3,
    'spreading_factor': 12,
    'coding_rate': 8,
    'preamble_length': 8,
    'implicitHeader': False,
    'sync_word': 0x12,
    'enable_CRC': False,
    'invert_IQ': False,
    'debug': True,
}

lora_pins = {
    'dio_0': 2,
    'ss': 5,
    'reset': 14,
    'sck': 18,
    'miso': 19,
    'mosi': 23,
}

status_led = {
    'failure': 32,
    'success': 33
}

network_settings = {
    'ssid': '',
    'password': '',
    'hostname': 'LORA-GATEWAY'
}

mqtt_settings = {
    'server': '',
    'client_id': 'lora-mqtt-gateway',
    'user': 'lora_mqtt_bridge',
    'password': '',
    'use_ssl': True,
    'default_topic': '/lora-mqtt-gateway'
}
