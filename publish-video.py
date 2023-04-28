# python3.9

# pip install paho-mqtt
# pip install opencv-python

import cv2
import random
import time

from paho.mqtt import client as mqtt_client


BROKER = '<emqx-broker-ip>'
# PORT = 1883
PORT = <port>

# TOPIC = " SUBCRIBE AND PUBLISH TO AN EMQX-MQTT BROKER "
TOPIC = "camstream/1"
# generate client ID with pub prefix randomly
CLIENT_ID = "publisher-1-video-{id}".format(id=random.randint(0, 1000))

USERNAME = '<username>'
PASSWORD = '<password>'

cam = cv2.VideoCapture(0)

def connect_mqtt():
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


def publish(client):
    msg_count = 0
    while True:
        # time.sleep(1)
        msg = f"messages: {msg_count}"

        _ , img = cam.read()
        #img = cv2.resize(img, (640 ,480))  # to reduce resolution 
        img_str = cv2.imencode('.jpg', img)[1].tobytes()

        result = client.publish(TOPIC, img_str)
        # result: [0, 1]
        status = result[0]
        if status == 0:
            print(f"Send `{msg}` to topic `{TOPIC}`")
        else:
            print(f"Failed to send message to topic {TOPIC}")
        msg_count += 1


def run():
    client = connect_mqtt()
    client.loop_start()
    publish(client)


if __name__ == '__main__':
    run()
