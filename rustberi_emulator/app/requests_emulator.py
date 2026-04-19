import time
import requests
import random
from datetime import datetime
import os
# Юзай этот ip
SERVER_URL = os.environ.get("SERVER_URL", "http://10.219.180.1:8082")
DEVICE_ID = os.environ.get("DEVICE_ID", "mai-0")


def generate_point():
    return {
        "time": datetime.utcnow().isoformat(),
        "x": random.uniform(0, 10),
        "y": random.uniform(0, 10),
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