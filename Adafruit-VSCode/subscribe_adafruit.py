import paho.mqtt.client as mqtt
from Adafruit_IO import Client

# Adafruit IO settings
adafruit_username = 'I4n'
adafruit_key = '///ADAFRUIT KEY HERE////////'
feed_name = 'led'  # Replace with your feed name

# MQTT Broker settings
mqtt_broker = 'broker.mqtt.cool'  # Replace with your MQTT broker address
mqtt_topic = 'wokwi-raspberry_mqtt_light_status'
mqtt_port = 1883  # Default MQTT port

# Create an instance of the Adafruit_IO Client
aio = Client(adafruit_username, adafruit_key)

# Callback function when a message is received from MQTT
def on_message(client, userdata, msg):
    import json  # Add this at the top of your script

def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode())  # Parse JSON payload
        light_status = payload.get("LED")  # Get LED status from payload

        if light_status is not None:
            print(f"Received LED status: {light_status}")

            # Send to Adafruit IO feed
            aio.send(feed_name, light_status)
            print(f"Sent {light_status} to Adafruit IO feed '{feed_name}'")
        else:
            print("LED key not found in payload.")
    except json.JSONDecodeError:
        print("Failed to decode JSON from message.")
    except Exception as e:
        print(f"Error handling message: {e}")


# Create an MQTT client instance
mqtt_client = mqtt.Client()

# Assign the on_message callback function
mqtt_client.on_message = on_message

# Connect to the MQTT broker
mqtt_client.connect(mqtt_broker, mqtt_port, 60)

# Subscribe to the desired topic
mqtt_client.subscribe(mqtt_topic)

# Start the MQTT loop to listen for messages
mqtt_client.loop_start()

# Keep the script running
try:
    while True:
        pass
except KeyboardInterrupt:
    print("Exiting...")
    mqtt_client.loop_stop()
