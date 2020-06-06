import lib.uasyncio as uasyncio
from lib.sx127x import SX127x
from lib.mqtt import MQTTClient
from lib.uasyncio.queues import Queue

from machine import Pin, SPI
import network
import time
import config
from helpers import transfrom_payload, is_connected

success_led = Pin(config.status_led['success'], Pin.OUT)
failure_led = Pin(config.status_led['failure'], Pin.OUT)


def raiseFailure(failed=True):
    if failed:
        failure_led.on()
    else:
        failure_led.off()


async def raiseSuccess():
    raiseFailure(False)
    success_led.on()
    await uasyncio.sleep_ms(100)
    success_led.off()


def setupLora():
    lora_spi = SPI(
        baudrate=10000000, polarity=0, phase=0,
        bits=8, firstbit=SPI.MSB,
        sck=Pin(config.lora_pins['sck'], Pin.OUT, Pin.PULL_DOWN),
        mosi=Pin(config.lora_pins['mosi'], Pin.OUT, Pin.PULL_UP),
        miso=Pin(config.lora_pins['miso'], Pin.IN, Pin.PULL_UP),
    )

    lora = SX127x(lora_spi, pins=config.lora_pins,
                  parameters=config.lora_settings)

    return lora


def setupWifi():
    print('Connecting to ', config.network_settings['ssid'])

    station = network.WLAN(network.STA_IF)

    station.active(True)
    station.connect(
        config.network_settings['ssid'], config.network_settings['password'])
    station.config(dhcp_hostname='LORA-GATEWAY')

    while station.isconnected() == False:
        pass

    print('WiFi Connection successful')

    return station


def setupMqtt():
    mqtt_client = MQTTClient(client_id=config.mqtt_settings['client_id'], server=config.mqtt_settings['server'],
                             user=config.mqtt_settings['user'], password=config.mqtt_settings['password'], ssl=config.mqtt_settings['use_ssl'])
    try:
        mqtt_client.connect()
    except:
        print('Failed to connect to MQTT')
        raiseFailure()

    return mqtt_client


async def messageWorker(mqtt_client, station):
    print("Running Worker")
    while True:
        result = await(q.get())
        topic, payload = transfrom_payload(result[0])

        for attempt in range(10):
            try:
                print('Trying publish', payload, 'on topic',
                      topic, ' in attempt', attempt)
                mqtt_client.publish(
                    config.mqtt_settings['default_topic'], result[0])
                mqtt_client.publish(topic, payload)
            except:
                if (station.isconnected() == False):
                    setupWifi()

                if (station.isconnected() == True and is_connected() == True):
                    try:
                        mqtt_client.connect()
                    except:
                        print('Failed to connect to MQTT')
            else:
                loop.create_task(raiseSuccess())
                break
        else:
            raiseFailure()


def onReceive(lora, payload):
    try:
        payload = payload.decode()
        rssi = lora.packetRssi()

        q.put_nowait([payload, rssi])
    except Exception as e:
        print(e)


station = setupWifi()
mqtt_client = setupMqtt()

lora = setupLora()
lora.onReceive(onReceive)
lora.receive()

q = Queue()
loop = uasyncio.get_event_loop()
message_worker = loop.create_task(messageWorker(mqtt_client, station))

try:
    loop.run_forever()
except KeyboardInterrupt:
    pass
finally:
    print("Closing Loop")
    loop.close()
