from typing import Union
from fastapi import FastAPI

app = FastAPI()


@app.get("/events/")
def get_event(
    event_id: Union[int, None] = None, 
    limit: Union[int, None] = None, 
    page: Union[int, None] = None,
    sensor_id: Union[int, None] = None,
    temperature: Union[float, None] = None,
    humidity: Union[float, None] = None,
):
    return {
        "event_id": event_id, 
        "limit": limit, 
        "page": page,
        "sensor_id": sensor_id,
        "temperature": temperature,
        "humidity": humidity,
    }
