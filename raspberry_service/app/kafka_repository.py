from kafka import KafkaProducer
import json
import os

BOOTSTRAP_SERVER =os.environ.get("BOOTSTRAP_SERVER", "10.219.180.1:9092")
REGION_INDEX=0
DEVICE_INDEX=1
class KafkaRepository:
    def __init__(self):
        self.producer = KafkaProducer(
        bootstrap_servers=BOOTSTRAP_SERVER,
        value_serializer=lambda v: json.dumps(v).encode("utf-8")
        )

    def send_to_kafka(self, device_id, info:dict):
        info["device_id"] = device_id
        topic = device_id.split("-")[REGION_INDEX]
        self.producer.send(topic, info)
        self.producer.flush()