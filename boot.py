import gc
import time
import machine
import micropython
import network
import esp
from lib.mqtt import MQTTClient
import lib.ntptime as ntptime

esp.osdebug(None)
gc.collect()

network_settings = {
    'ssid': 'YOUR_SSID',
    'password': 'YOUR_WIFI_PASSWORD',
    'hostname': 'LORA-GATEWAY'
}

mqtt_settings = {
    'server': 'YOUR_MQTT_SERVER_ADDRESS',
    'client_id': 'lora-mqtt-gateway',
    'user': 'YOUR_MQTT_USER',
    'password': 'YOUR_MQTT_PASSWORD',
    'use_ssl': True,
    'default_topic': '/lora-mqtt-gateway'
}

print('Connecting to ', network_settings['ssid'])
station = network.WLAN(network.STA_IF)

station.active(True)
station.connect(network_settings['ssid'], network_settings['password'])
station.config(dhcp_hostname='LORA-GATEWAY')

while station.isconnected() == False:
    pass

print('WiFi Connection successful')

try:
    ntptime.settime()
    print('RTC Updated time is', time.time())
except OSError as e:
    print('Unable to update RTC from NTP server')
    print('Resetting in 5 seconds')
    time.sleep(5)
    machine.reset()

try:
    print('Connecting to MQTT Broker')
    mqtt_client = MQTTClient(client_id=mqtt_settings['client_id'], server=mqtt_settings['server'],
                             user=mqtt_settings['user'], password=mqtt_settings['password'], ssl=mqtt_settings['use_ssl'])
    mqtt_client.connect()
except OSError as e:
    print('Failed to connect to MQTT Broker.')
    print('Resetting in 5 seconds')
    time.sleep(5)
    machine.reset()
