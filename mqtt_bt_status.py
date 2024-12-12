#!/usr/bin/env python3

import dotenv
import json
import os
import time

import paho.mqtt.client as mqtt

dotenv.load_dotenv()

username = os.getenv("MQTT_USERNAME")
password = os.getenv("MQTT_PASSWORD")
broker_address = os.getenv("MQTT_HOSTNAME")
broker_port = int(os.getenv("MQTT_PORT"))

if not username or not password or not broker_address or not broker_port:
    raise RuntimeError("Missing configuration")

try:
    unique_id_file = open("unique_id")
    unique_id = unique_id_file.read().strip()

except FileNotFoundError:
    print("Unique ID file not found")
    raise

discovery_prefix = os.getenv("MQTT_DISCOVERY_PREFIX", "homeassistant")
topic_prefix = "gamepad_status"


def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Connected with result code {reason_code}")


def on_message(client, userdata, msg):
    print(f"{msg.topic} {msg.payload}")


def on_publish(client, userdata, mid, reason_code, properties):
    print("Published")
    print(mid)


client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.on_message = on_message
client.on_publish = on_publish

client.username_pw_set(username, password)
client.connect(broker_address, broker_port, 60)

client.loop_start()

config_topic = f"{discovery_prefix}/device/gamepad/config"
connected_state_topic = f"{topic_prefix}/connected"
battery_state_topic = f"{topic_prefix}/battery"

payload = {
    "dev": {
        "ids": unique_id,
        "name": "Gamepad",
    },
    "o": {
        "name": "mqtt_bt_status",
        "sw": "0.1",
        "url": "https://github.com/lilveg/mqtt_bt_status",
    },
    "cmps": {
        "connected": {
            "p": "binary_sensor",
            "device_class": "connectivity",
            "unique_id": f"{unique_id}_connected",
            "state_topic": connected_state_topic,
        },
        "battery": {
            "p": "sensor",
            "device_class": "battery",
            "unique_id": f"{unique_id}_battery",
            "state_topic": battery_state_topic,
        },
    },
    "qos": 2,
}

print(config_topic)
print(json.dumps(payload))
msg_info = client.publish(config_topic, json.dumps(payload), qos=2)

time.sleep(2)

client.loop_stop()
