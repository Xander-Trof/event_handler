from fastapi import FastAPI
from .api.events import events_router

app = FastAPI()

app.include_router(events_router)
