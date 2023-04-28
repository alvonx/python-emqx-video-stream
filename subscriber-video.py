# python3.9

# pip install paho-mqtt
# pip install opencv-python

import json
import cv2
import random
import numpy as np
from paho.mqtt import client as mqtt_client


BROKER = '<emqx-broker-ip>'
# PORT = 1883
PORT = <port>

# TOPIC = " SUBCRIBE AND PUBLISH TO AN EMQX-MQTT BROKER "
TOPIC = "camstream/1"
# generate client ID with pub prefix randomly
CLIENT_ID = "subscriber-1-video-{id}".format(id=random.randint(0, 1000))

USERNAME = '<username>'
PASSWORD = '<password>'


def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(CLIENT_ID)
    client.username_pw_set(USERNAME, PASSWORD)
    client.on_connect = on_connect
    client.connect(BROKER, PORT)
    return client


def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        # received_message = msg.payload.decode()
        # received_message_json = json.loads(received_message)
        # print(received_message_json['message_id'])
        # print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
         
        # nparr = np.frombuffer(received_message_json['image_data'], np.uint8)
        nparr = np.frombuffer(msg.payload, np.uint8)
        frame = cv2.imdecode(nparr,  cv2.IMREAD_COLOR)

        #frame= cv2.resize(frame, (640,480))   # just in case you want to resize the viewing area
        cv2.imshow('recv', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            return
        

    client.subscribe(TOPIC)
    client.on_message = on_message


def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()


if __name__ == '__main__':
    run()
