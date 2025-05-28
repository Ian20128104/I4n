import paho.mqtt.client as mqtt

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Connected with result code {reason_code}")
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("wokwi-weather")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    # print(msg.topic+" "+str(msg.payload))
    utf = msg.payload.decode('utf-8')
    print(utf)
    if 'hello' in utf:
        mqttc.publish('wokwi-weather', 'Hello back')
        print('hello.......................')

mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqttc.on_connect = on_connect
mqttc.on_message = on_message

mqttc.connect("broker.mqtt.cool", 1883, 60)
#  mqttc.publish('wokwi-weather','You message goes here')
mqttc.loop_forever()