from Adafruit_IO import Client
import paho.mqtt.client as mqtt
import time

# --- Adafruit IO Setup ---
ADAFRUIT_IO_USERNAME = 'I4n'
ADAFRUIT_IO_KEY = '/////ADA FRUIT KEY HERE//////'
FEED_KEY = 'button'

aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

# --- MQTT Broker Setup ---
MQTT_BROKER = 'broker.mqtt.cool'
MQTT_PORT = 1883  # or 8883 for TLS
MQTT_TOPIC = 'Wokwi-MicropythonW_light-status'

mqtt_client = mqtt.Client()

def publish_to_broker(value):
    mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
    mqtt_client.loop_start()
    mqtt_client.publish(MQTT_TOPIC, payload=value, qos=1)
    mqtt_client.loop_stop()
    mqtt_client.disconnect()

# --- Main Loop ---
while True:
    try:
        data = aio.receive(FEED_KEY)
        print(f"Fetched value from Adafruit IO: {data.value}")
        publish_to_broker(data.value)
    except Exception as e:
        print(f"Error: {e}")

    time.sleep(10)  # adjust interval as needed
