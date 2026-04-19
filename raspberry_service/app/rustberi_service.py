from fastapi import FastAPI
import uvicorn
import os
from pydantic import BaseModel
from fastapi import status

from kafka_repository import KafkaRepository
from redis_repository import RedisRepository


PORT_FAST_API = int(os.environ.get("PORT_FAST_API", 8080))
HOST_FAST_API = os.environ.get("HOST_FAST_API", "0.0.0.0")

app = FastAPI(
    title="Rustberi API",
    description="API для работы с точками",
    version="1.0.0"
)

repo = RedisRepository()
kafka = KafkaRepository()


class PointInfo(BaseModel):
    time: str
    x: float
    y: float


@app.post("/add_point/{device_id}", tags=["Points"])
async def create_data(device_id: str, point: PointInfo):
    if(point.time is not  None):
        repo.set_point(device_id, point.model_dump())
        kafka.send_to_kafka(device_id, point.model_dump())

    return {
        "status": "saved",
        "device_id": device_id,
        "point": point
    }


@app.get("/health", tags=["Health"], status_code=status.HTTP_200_OK)
def root():
    return {"status": "ok"}


if __name__ == "__main__":
    uvicorn.run(
        "rustberi_service:app",
        host=HOST_FAST_API,
        port=PORT_FAST_API,
        reload=True
    )