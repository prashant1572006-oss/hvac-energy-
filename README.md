# HVAC Energy Optimisation Using IoT

## Project Overview

This project focuses on monitoring and optimising HVAC (Heating, Ventilation and Air Conditioning) energy consumption using IoT technologies.

The system collects environmental and HVAC operating data and sends it through MQTT to a cloud broker. The data is then displayed on a real-time Streamlit dashboard for monitoring and analysis.

## Objectives

- Monitor temperature and humidity.
- Monitor occupancy.
- Monitor HVAC fan speed.
- Calculate voltage, current and power consumption.
- Transmit data using MQTT.
- Use HiveMQ Cloud as the MQTT broker.
- Display real-time data through a Streamlit dashboard.
- Identify opportunities for reducing unnecessary HVAC energy consumption.

## Technologies Used

- Python
- Streamlit
- MQTT
- HiveMQ Cloud
- Paho MQTT
- Plotly
- Git
- GitHub

## System Architecture

```text
Synthetic Sensor Data
        ↓
      MQTT
        ↓
   HiveMQ Cloud
        ↓
Streamlit Dashboard
