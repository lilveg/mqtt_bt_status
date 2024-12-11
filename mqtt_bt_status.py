#!/usr/bin/env python3

import dotenv
import os
import time

import paho.mqtt.client as mqtt

dotenv.load_dotenv()

hostname = "test_mqtt"
topic = "test_topic"
username = os.getenv("MQTT_USERNAME")
password = os.getenv("MQTT_PASSWORD")
broker_address = os.getenv("MQTT_HOSTNAME")
broker_port = int(os.getenv("MQTT_PORT"))

if not username or not password or not broker_address or not broker_port:
    raise RuntimeError("Missing configuration")

def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Connected with result code {reason_code}")
    client.subscribe("$SYS/#")

def on_message(client, userdata, msg):
    print(f"{msg.topic} {msg.payload}")

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.on_message = on_message

client.username_pw_set(username, password)
client.connect(broker_address, broker_port, 60)
client.loop_forever()

