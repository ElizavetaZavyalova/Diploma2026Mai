from fastapi import FastAPI
import uvicorn
import os
from fastapi import status

from clichouse_repository import ClickhouseRepository
from redis_repository import RedisRepository


PORT_FAST_API = int(os.environ.get("PORT_FAST_API", 8080))
HOST_FAST_API = os.environ.get("HOST_FAST_API", "0.0.0.0")

app = FastAPI(
    title="Rustberi API",
    description="API для работы с точками",
    version="1.0.0"
)

repo = RedisRepository()
clickhouse= ClickhouseRepository()

from fastapi import FastAPI

app = FastAPI()
@app.get("/point/{device_id}", tags=["Points"])
async def get_point(device_id: str):
    return repo.get_point(device_id)
@app.get("/point_history/{region}/{device_id}/{count}", tags=["Points"])
async def get_last_point_history(device_id: str, region:str, count: int):
    return clickhouse.get_last_points(count=count, region=region, device_id=device_id)
@app.get("/points/", tags=["Points"])
async def get_point(device_ids: list):
    return repo.get_points(device_ids)


@app.get("/health", tags=["Health"], status_code=status.HTTP_200_OK)
def root():
    return {"status": "ok"}


if __name__ == "__main__":
    uvicorn.run(
        "gui_service:app",
        host=HOST_FAST_API,
        port=PORT_FAST_API,
        reload=True
    )