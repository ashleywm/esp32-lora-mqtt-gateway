from machine import Pin, SPI
from lib.sx127x import SX127x
from src.mqtt_sender import MqttMessage
from src.utils import transfrom_payload


lora_default = {
    'frequency': 433E6,
    'frequency_offset': 0,
    'tx_power_level': 14,
    'signal_bandwidth': 125E3,
    'spreading_factor': 9,
    'coding_rate': 5,
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

lora_spi = SPI(
    baudrate=10000000, polarity=0, phase=0,
    bits=8, firstbit=SPI.MSB,
    sck=Pin(lora_pins['sck'], Pin.OUT, Pin.PULL_DOWN),
    mosi=Pin(lora_pins['mosi'], Pin.OUT, Pin.PULL_UP),
    miso=Pin(lora_pins['miso'], Pin.IN, Pin.PULL_UP),
)

lora = SX127x(lora_spi, pins=lora_pins, parameters=lora_default)


def onReceive(lora, payload):
    try:
        payload = payload.decode()
        rssi = lora.packetRssi()

        raw_message = MqttMessage(
            mqtt_settings['default_topic'], {'payload': payload, 'rssi': rssi})
        raw_message.send(mqtt_client)

        transformed_message = transfrom_payload(payload)
        transformed_message.send(mqtt_client)
    except Exception as e:
        print(e)


if __name__ == '__main__':
    print("LoRa MQTT Gateway Started")
    lora.onReceive(onReceive)
    lora.receive()
