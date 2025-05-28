import time
from machine import Pin
import network
import socket as socket
import ujson
from umqtt import MQTTClient

# https://mqtt.aarsoftwareserver.com:444/test_client/

# MQTT Server Parameters
MQTT_CLIENT_ID = "micropython-mqtt-test"
MQTT_BROKER    = "broker.mqtt.cool" # BROKER SETTING
MQTT_USER      = ""
MQTT_PASSWORD  = ""
MQTT_TOPIC     = "Wokwi-MicropythonW_light-status" # TOPIC TO SUBSCRIBE TO
Button_Pressed = 0

# Connect to Wi-Fi
print("Connecting to WiFi...")
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect('Wokwi-GUEST', '')
while not wifi.isconnected():
    print(".", end="")
    time.sleep(0.1)
print("Connected!")

print("Connecting to MQTT server... ", end="")
client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER, user=MQTT_USER, password=MQTT_PASSWORD)
client.connect()
print("Connected To Broker!!!")

# Establish button and led
button = Pin(28, Pin.IN, Pin.PULL_UP)
led = Pin("LED", Pin.OUT)

# Read state of the push button
# Turn on the onboard LED
prev_value = "off"
while True:
    message = ujson.dumps({
        "Button": button.value(),
        "LED": led.value(),
        "Button presses": Button_Pressed,
    })
    if button.value() == 0:
        led.value(1)
        if prev_value == "off":
            prev_value = "on"
            Button_Pressed += 1
            print(Button_Pressed)
            client.publish(MQTT_TOPIC, message)
    else:
        led.value(0)
        if prev_value == "on":
            prev_value = "off"
            client.publish(MQTT_TOPIC, message)
    time.sleep(1)
