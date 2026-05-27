from fastapi import FastAPI
import uvicorn
import os
from fastapi import status
import random
from redis_repository import RedisRepository
from fastapi import FastAPI


PORT_FAST_API = int(os.environ.get("PORT_FAST_API", 8080))
HOST_FAST_API = os.environ.get("HOST_FAST_API", "0.0.0.0")

app = FastAPI(
    title="Rustberi API",
    description="API для работы с точками",
    version="1.0.0"
)

repo = RedisRepository()


app = FastAPI()

def count_points(angle1, lat1, lon1, angle2, lat2, lon2):
    return [{"lat":  random.uniform(50.23, 50.24), "lon": random.uniform(36.01, 36.02)}]

@app.get("/point/{device_id}", tags=["Points"])
async def get_point(device_id: str):
    return repo.get_point(device_id)
@app.get("/points/{device1}/{device2}", tags=["Points"])
async def get_point(device1, device2):
    response=repo.get_points([device1, device2])
    c1 = response[0].current
    c2 = response[1].current

    res=count_points(
        c1["angle"], c1["lat"], c1["lon"],
        c2["angle"], c2["lat"], c2["lon"]
    )
    return {"markers":res}

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