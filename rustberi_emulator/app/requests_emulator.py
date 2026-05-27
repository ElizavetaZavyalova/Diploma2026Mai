import time
import requests
import random
from datetime import datetime
import os
# Юзай этот ip
SERVER_URL = os.environ.get("SERVER_URL", "http://10.219.180.1:8082")
DEVICE_ID = os.environ.get("DEVICE_ID", "mai-0")
LAT = float(os.environ.get("LAT", "55.46"))
LON = float(os.environ.get("LON", "37.37"))

def generate_point():
    return {
        "time": datetime.utcnow().isoformat(),
        "angle": random.uniform(0, 360),
        "lat": LAT,
        "lon": LON
    }


def send_point():
    url = f"{SERVER_URL}/add_point/{DEVICE_ID}"
    data = generate_point()

    try:
        response = requests.post(url, json=data, timeout=5)
        print(f"[{response.status_code}] sent:", data)
    except Exception as e:
        print("Error:", e)


if __name__ == "__main__":
    while True:
        send_point()
        time.sleep(1)