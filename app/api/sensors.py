from typing import Annotated

from fastapi import APIRouter, Body

from app.db.client import db_client

from .schema import SensorParams

sensors_router = APIRouter()


@sensors_router.get("/sensor/{sensor_id}")
def get_sensor_by_id(sensor_id: int):
    return {
        "sensor": db_client.get_sensor_by_id(sensor_id),
    }


@sensors_router.post("/sensor/")
def post_sensor(sensor: Annotated[SensorParams, Body(embed=False)]):
    sensor = db_client.create_sensor(sensor)
    return {"sensor_id": sensor.id}


@sensors_router.put("/sensor/{sensor_id}")
def put_sensor(sensor_id: int, sensor: Annotated[SensorParams, Body(embed=False)]):
    return {"sensor": db_client.update_sensor_by_id(sensor_id, sensor)}


@sensors_router.delete("/sensor/{sensor_id}")
def delete_sensor(sensor_id: int):
    db_client.delete_sensor(sensor_id)
    return
