from fastapi import FastAPI
import uvicorn
import os
from pydantic import BaseModel

from RustberiService.redis_repository import RedisRepository


PORT_FAST_API = int(os.environ.get("PORT_FAST_API", 8080))
HOST_FAST_API = os.environ.get("HOST_FAST_API", "0.0.0.0")

app = FastAPI(
    title="Rustberi API",
    description="API для работы с точками",
    version="1.0.0"
)

repo = RedisRepository()


class PointInfo(BaseModel):
    time: str
    x: float
    y: float


@app.post("/add_point/{device_id}", tags=["Points"])
def create_data(device_id: str, point: PointInfo):
    repo.set_point(device_id, point.model_dump())

    return {
        "status": "saved",
        "device_id": device_id,
        "point": point
    }


@app.get("/", tags=["Health"])
def root():
    return {"status": "ok"}


if __name__ == "__main__":
    uvicorn.run(
        "rustberi_service:app",
        host=HOST_FAST_API,
        port=PORT_FAST_API,
        reload=True
    )