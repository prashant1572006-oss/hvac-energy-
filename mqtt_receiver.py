import paho.mqtt.client as mqtt
import json

BROKER = "1fba33fd31ce4a0896588cb3c09ba4e2.s1.eu.hivemq.cloud"
PORT = 8883

USERNAME = "hvac user"
PASSWORD = "hvac1234"

TOPIC = "hvac/sensors"


def on_connect(client, userdata, flags, reason_code, properties):
    print("Connected to HiveMQ!")
    client.subscribe(TOPIC)
    print("Subscribed to:", TOPIC)


def on_message(client, userdata, msg):
    data = json.loads(msg.payload.decode())

    print("Received HVAC data:")
    print(data)
    print()


client = mqtt.Client(
    mqtt.CallbackAPIVersion.VERSION2,
    client_id="hvac-dashboard-receiver"
)

client.username_pw_set(USERNAME, PASSWORD)

client.tls_set()

client.on_connect = on_connect
client.on_message = on_message

print("Connecting to HiveMQ...")

client.connect(BROKER, PORT)

client.loop_forever()
