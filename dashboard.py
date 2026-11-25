import streamlit as st
import paho.mqtt.client as mqtt
import json
import time

# -----------------------------
# HiveMQ settings
# -----------------------------

BROKER = "1fba33fd31ce4a0896588cb3c09ba4e2.s1.eu.hivemq.cloud"
PORT = 8883

USERNAME = "hvac user"
PASSWORD = "hvac1234"

TOPIC = "hvac/sensors"


# -----------------------------
# MQTT connection
# -----------------------------

@st.cache_resource
def start_mqtt():

    latest_data = {
        "data": None
    }

    def on_connect(client, userdata, flags, reason_code, properties):

        print("Dashboard connected to HiveMQ!")

        client.subscribe(TOPIC)

        print("Dashboard subscribed to:", TOPIC)


    def on_message(client, userdata, msg):

        try:

            data = json.loads(
                msg.payload.decode()
            )

            latest_data["data"] = data

            print("Dashboard received:", data)

        except Exception as e:

            print("MQTT error:", e)


    client = mqtt.Client(
        mqtt.CallbackAPIVersion.VERSION2,
        client_id="hvac-streamlit-dashboard"
    )

    client.username_pw_set(
        USERNAME,
        PASSWORD
    )

    client.tls_set()

    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(
        BROKER,
        PORT
    )

    client.loop_start()

    return latest_data


mqtt_data = start_mqtt()


# -----------------------------
# Streamlit page
# -----------------------------

st.set_page_config(
    page_title="HVAC Energy Optimisation",
    page_icon="❄️",
    layout="wide"
)


st.title("❄️ HVAC Energy Optimisation Using IoT")

st.caption(
    "Live data received through MQTT and HiveMQ Cloud"
)


# -----------------------------
# Auto-refresh section
# -----------------------------

@st.fragment(run_every="2s")
def dashboard():

    data = mqtt_data["data"]

    if data is None:

        st.warning(
            "Waiting for HVAC data from HiveMQ..."
        )

        return


    # -------------------------
    # Live parameters
    # -------------------------

    st.subheader("📡 Live HVAC Parameters")

    col1, col2, col3, col4 = st.columns(4)


    col1.metric(
        "🌡️ Temperature",
        f"{data['temperature']:.2f} °C"
    )


    col2.metric(
        "💧 Humidity",
        f"{data['humidity']:.2f} %"
    )


    occupancy = (
        "YES"
        if data["occupancy"] == 1
        else "NO"
    )


    col3.metric(
        "👤 Occupancy",
        occupancy
    )


    col4.metric(
        "🌀 Fan Speed",
        f"{data['fan_speed']} %"
    )


    # -------------------------
    # Energy monitoring
    # -------------------------

    st.divider()

    st.subheader("⚡ Energy Monitoring")


    col1, col2, col3 = st.columns(3)


    col1.metric(
        "Voltage",
        f"{data['voltage']} V"
    )


    col2.metric(
        "Current",
        f"{data['current']} A"
    )


    col3.metric(
        "Power",
        f"{data['power']} W"
    )


    # -------------------------
    # HVAC status
    # -------------------------

    st.divider()

    st.subheader("🌀 HVAC Status")


    fan = data["fan_speed"]


    if fan == 0:

        st.success("HVAC OFF")


    elif fan <= 60:

        st.info("HVAC LOW / MEDIUM")


    else:

        st.warning("HVAC HIGH")


    # -------------------------
    # Latest MQTT message
    # -------------------------

    st.divider()

    st.subheader("📨 Latest MQTT Data")

    st.json(data)


dashboard()
