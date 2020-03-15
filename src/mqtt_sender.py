class MqttMessage:
    def __init__(self, topic, payload):
        self.topic = topic
        self.payload = payload

    def send(self, client):
        if client is None:
            print('MQTT Client not connected')
            return

        print(self.topic, self.payload)

        client.check_msg()
        client.publish(self.topic, str(self.payload))
