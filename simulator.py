import csv
import random
import time
import os
from datetime import datetime

FILE = "hvac_data.csv"

# Create CSV file if it doesn't exist
if not os.path.exists(FILE):
    with open(FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "time",
            "temperature",
            "humidity",
            "occupancy",
            "fan_speed",
            "voltage",
            "current",
            "power",
            "energy"
        ])

energy = 0

while True:

    # Simulated sensor values
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

    # Simulated electrical values
    voltage = 12
    current = round((fan_speed / 100) * 0.45, 3)
    power = round(voltage * current, 2)

    # Energy in kWh
    energy += power * (5 / 3600) / 1000

    # Save data
    with open(FILE, "a", newline="") as f:
        writer = csv.writer(f)

        writer.writerow([
            datetime.now().strftime("%H:%M:%S"),
            temperature,
            humidity,
            occupancy,
            fan_speed,
            voltage,
            current,
            power,
            round(energy, 5)
        ])

    print(
        f"Temp={temperature}°C | "
        f"Humidity={humidity}% | "
        f"Occupancy={occupancy} | "
        f"Fan={fan_speed}% | "
        f"Power={power}W"
    )

    time.sleep(5)
