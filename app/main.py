from fastapi import FastAPI
from .api.events import events_router
from .api.sensors import sensors_router

app = FastAPI()

app.include_router(events_router)
app.include_router(sensors_router)
