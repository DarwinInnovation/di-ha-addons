#!/usr/bin/env python3
import argparse
import json
import os
import sys
import time
import csv
import requests
import uuid
import base64
import hashlib
import hmac


from pathlib import Path
from datetime import datetime

import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish

# open token
TOKEN = os.environ["SWITCHBOT_TOKEN"] #'7ea000fbd7a6ea177550cabcac46d8abb0b06bef8f195ec372bcb3c53021c304b0853145d8b8dc10127ffb2641def544' # copy and paste from the SwitchBot app V6.14 or later
# secret key
SECRET = os.environ["SWITCHBOT_SECRET"] #'c3d299f88b1f98532cfab9f5195253ab' # copy and paste from the SwitchBot app V6.14 or later

class SwitchBotSensor:
    def __init__(self, device, type):
        self.device = device
        self.type = type

        name = f"{self.device.name} {self.type}"
        self.name = name
        self.config_topic = f"homeassistant/sensor/{self.device.name}/{self.type}/config"


    def get_config(self):
        return {
            "unique_id": f"{self.device.device_id}-{self.type}",
            "device_class": f"{self.type}",
            "name": f"{self.device.device_name} {self.type}",
            "state_topic": self.device.state_topic,
        }

class SwitchBotTemperature(SwitchBotSensor):
    def __init__(self, device):
        super().__init__(device, "temperature")

    def get_config(self):
        config = super().get_config()
        config["device_class"] = "temperature"
        config["unit_of_measurement"] = "°C"
        config["icon"] = "hass:thermometer"
        config["value_template"] = "{{ value_json.temperature }}"
        return config

class SwitchBotHumidity(SwitchBotSensor):
    def __init__(self, device):
        super().__init__(device, "humidity")

    def get_config(self):
        config = super().get_config()
        config["device_class"] = "humidity"
        config["unit_of_measurement"] = "%"
        config["icon"] = "hass:water-percent"
        config["value_template"] = "{{ value_json.humidity }}"
        return config


SWITCHBOT_SENSORS = {
    "temperature": SwitchBotTemperature,
    "humidity": SwitchBotHumidity,
}

class SwitchBotDevice:
    def __init__(self, device_object, sbcloud):
        self.device_id = device_object['deviceId']
        self.device_name = device_object['deviceName']
        self.device_type = device_object['deviceType']

        name = f"switchbot-{self.device_id}"
        self.name = name
        #self.config_topic = f"homeassistant/sensor/{name}/config"
        self.state_topic = f"homeassistant/sensor/{name}/state"

        self.headers = sbcloud.headers

    def get_status(self):
        status = {}

        url = f'https://api.switch-bot.com/v1.0/devices/{self.device_id}/status'
        response = requests.get(url, headers=self.headers).json()

        if response['statusCode'] != 100:
            return status

        for key, value in response['body'].items():
            if key == 'deviceId' or key == 'deviceName' or key == 'deviceType' or key == 'hubDeviceId':
                continue
            status[key] = value

        return status

    def publish_status(self, client):
        status = self.get_status()

        print(f"Publishing {self.state_topic}: {json.dumps(status)}")
        client.publish(
            self.state_topic,
            payload=json.dumps(status),
            retain=True,
        )

        return status

    def publish_config(self, client):
        status = self.get_status()

        for key, value in status.items():
            if key in SWITCHBOT_SENSORS:
                sensor = SWITCHBOT_SENSORS[key](self)
                print(f"Publishing {sensor.config_topic}: {json.dumps(sensor.get_config())}")
                client.publish(
                    sensor.config_topic,
                    payload=json.dumps(sensor.get_config()),
                    retain=True,
                )
        

    def __str__(self):
        return f'{self.device_id} {self.device_name} {self.device_type}'

    def __repr__(self):
        return f'{self.device_id} {self.device_name} {self.device_type}'

# Class to handle connection to SwitchBot Cloud
class SwitchBotCloud:
    def __init__(self, token, secret):
        self.token = token
        self.secret = secret

        self.headers = self._auth_headers()

    def _auth_headers(self):
        # Declare empty header dictionary
        apiHeader = {}
        # open token
        token = self.token
        # secret key
        secret = self.secret
        nonce = uuid.uuid4()
        t = int(round(time.time() * 1000))
        string_to_sign = '{}{}{}'.format(token, t, nonce)

        string_to_sign = bytes(string_to_sign, 'utf-8')
        secret = bytes(secret, 'utf-8')

        sign = base64.b64encode(hmac.new(secret, msg=string_to_sign, digestmod=hashlib.sha256).digest())

        print ('Authorization: {}'.format(token))
        print ('t: {}'.format(t))
        print ('sign: {}'.format(str(sign, 'utf-8')))
        print ('nonce: {}'.format(nonce))

        #Build api header JSON
        apiHeader['Authorization']=token
        apiHeader['Content-Type']='application/json'
        apiHeader['charset']='utf8'
        apiHeader['t']=str(t)
        apiHeader['sign']=str(sign, 'utf-8')
        apiHeader['nonce']=str(nonce)

        return apiHeader

    def get_devices(self):
        self.headers = self._auth_headers()
        url = 'https://api.switch-bot.com/v1.1/devices'
        response = requests.get(url, headers=self.headers).json()
        print(response)
        
        devices = []

        if 'statusCode' not in response or response['statusCode'] != 100:
            return devices

        for device in response['body']['deviceList']:
            devices.append(SwitchBotDevice(device, self))

        return devices



def main(args):
    sbcloud = SwitchBotCloud(TOKEN, SECRET)

    client = mqtt.Client("ha-client")
    client.username_pw_set("hotwatertank", "9drM4HvbVo")
    client.connect(args.broker)
    client.loop_start()

    while True:
        need_config = True
        for device in sbcloud.get_devices():
            if need_config:
                device.publish_config(client)
                need_config = False
            status = device.publish_status(client)
            print(status)
            # if status is not None:
            #     client.publish(
            #         f"homeassistant/sensor/{args.name}/state",
            #         payload=status,
            #         retain=True,
            #     )
            #     print(f"Published {status} to {args.name}")
        time.sleep(args.delay)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-b", "--broker", help="Set broker", default="homeassistant.local"
    )
    parser.add_argument(
        "-n", "--name", help="Set last part of topic", default="waterTankLT"
    )
    parser.add_argument("-d", "--delay", help="Update period", default=120, type=int)
    args = parser.parse_args()

    try:
        main(args)
    except KeyboardInterrupt:
        pass
