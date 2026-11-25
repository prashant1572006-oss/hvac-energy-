import paho.mqtt.client as mqtt
import json
import random
import time

# --------------------------------
# HiveMQ Cloud settings
# --------------------------------

BROKER = "1fba33fd31ce4a0896588cb3c09ba4e2.s1.eu.hivemq.cloud"
PORT = 8883

USERNAME = "hvac user"
PASSWORD = "hvac1234"

TOPIC = "hvac/sensors"


# --------------------------------
# MQTT client
# --------------------------------

client = mqtt.Client(
    mqtt.CallbackAPIVersion.VERSION2,
    client_id="hvac-simulator"
)

client.username_pw_set(USERNAME, PASSWORD)

client.tls_set()


# --------------------------------
# Connect to HiveMQ
# --------------------------------

print("Connecting to HiveMQ...")

client.connect(BROKER, PORT)

client.loop_start()

print("Connected to HiveMQ!")
print("Publishing HVAC data...\n")


# --------------------------------
# Generate sensor data
# --------------------------------

while True:

    temperature = round(random.uniform(24, 31), 2)

    humidity = round(random.uniform(45, 75), 2)

    occupancy = random.choice([0, 1])


    # HVAC optimisation logic

    if occupancy == 0:

        fan_speed = 0

    elif temperature < 25:

        fan_speed = 0

    elif temperature < 28:

        fan_speed = 60

    else:

        fan_speed = 100


    # Electrical values

    voltage = 12

    current = round(
        (fan_speed / 100) * 0.45,
        3
    )

    power = round(
        voltage * current,
        2
    )


    # --------------------------------
    # Create MQTT message
    # --------------------------------

    data = {

        "temperature": temperature,

        "humidity": humidity,

        "occupancy": occupancy,

        "fan_speed": fan_speed,

        "voltage": voltage,

        "current": current,

        "power": power
    }


    message = json.dumps(data)


    # --------------------------------
    # Publish to HiveMQ
    # --------------------------------

    client.publish(
        TOPIC,
        message
    )


    print(message)


    time.sleep(5)
