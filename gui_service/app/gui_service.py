from fastapi import FastAPI
import uvicorn
import os

from redis_repository import RedisRepository


PORT_FAST_API = int(os.environ.get("PORT_FAST_API", 8080))
HOST_FAST_API = os.environ.get("HOST_FAST_API", "0.0.0.0")

app = FastAPI(
    title="Rustberi API",
    description="API для работы с точками",
    version="1.0.0"
)

repo = RedisRepository()


@app.get("/point/{device_id}", tags=["Points"])
async def get_point(device_id: str):
    return repo.get_point(device_id)

@app.get("/points/", tags=["Points"])
async def get_point(device_ids: list):
    return repo.get_points(device_ids)


@app.get("/", tags=["Health"])
def root():
    return {"status": "ok"}


if __name__ == "__main__":
    uvicorn.run(
        "gui_service:app",
        host=HOST_FAST_API,
        port=PORT_FAST_API,
        reload=True
    )