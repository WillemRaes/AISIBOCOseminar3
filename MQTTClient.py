"""

Helper class

"""

import paho.mqtt.client as mqtt
import time
import threading
import logging


class MQTTStreamConsumer(threading.Thread):
    def __init__(self, group=None, target=None, name=None, client_addr=None, client_info=None, topic=None, broker_addr=None,
                 queue_out=None):
        super(MQTTStreamConsumer, self).__init__()
        self.target = target
        self.name = name
        self.queue_out = queue_out
        self.broker_addr = broker_addr
        self.counter = 0
        self.topic = topic
        return

    # The callback for when the client receives a CONNACK response from the server.
    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code " + str(rc))

        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.

        client.subscribe(self.topic)
        # client.subscribe(HubConfig.imuTopic)
        # client.subscribe(HubConfig.environmentTopic)
        # client.subscribe(HubConfig.powerTopic)

    # The callback for when a PUBLISH message is received from the server.
    def on_message(self, client, userdata, message):
        server_time_ms = time.time()
        result = float(message.payload)
        # print(result)
        try:

            record = [message.topic, server_time_ms, result]
            if not self.queue_out.full():

                self.queue_out.put(record)


            else:
                self.counter += 1
                print("Dropped " + str(self.topic) + ": " + str(self.counter))
        except Exception as e:
            print(e)

    def run(self):
        no_data_counter = 0
        no_data_bool = 0

        client = mqtt.Client()
        client.on_connect = self.on_connect
        client.on_message = self.on_message
        client.connect(self.broker_addr, 1883, 60)
        # while True:
        client.loop_forever()
        # client.publish("wheelchair/whch1/power", "AFDCBD2F3D00E402")
        # client.publish("wheelchair/whch1/pressure", "C961FF0FFF1FFF2FFF3FFF4FFF5FFF6FFF7F")
        # client.publish("wheelchair/whch1/imu", "BA23F8FFD0FFDE03F2FEF100EEFF0600EAFFA8FF")
        # client.publish("wheelchair/whch1/environment", "CE2FC1080F27")
        #  time.sleep(1)

        return -1
