import time
from machine import Pin
import network
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

# Initialize button and led
button = Pin(28, Pin.IN, Pin.PULL_UP)
led = Pin("LED", Pin.OUT)

# MQTT callback to handle incoming messages
def mqtt_callback(topic, msg):
    try:
        msg_str = msg.decode('utf-8')
        print("Received message:", msg_str)
        data = ujson.loads(msg_str)
        if data.get("Button") == 1:
            print("Turning LED ON")
            led.value(1)  # Turn LED ON
            time.sleep(1)
        else:
            led.value(0)  # Turn LED OFF
    except Exception as e:
        print("Error parsing message:", e)

# Set the callback and subscribe to the topic
client.set_callback(mqtt_callback)
client.subscribe(MQTT_TOPIC)
print("Subscribed to topic:", MQTT_TOPIC)

prev_value = "off"

while True:
    # Check for incoming messages
    client.check_msg()

    # Prepare message to publish
    message = ujson.dumps({
        "Button": button.value(),
        "LED": led.value(),
        "Button presses": Button_Pressed,
    })

    # Detect button press
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
