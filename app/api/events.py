from typing import Annotated, Optional
from fastapi import APIRouter, Query, Body
from pydantic import BaseModel, Field, field_validator

events_router = APIRouter()


class FilterParams(BaseModel):
    limit: int = Field(1, gt=0, le=100) 
    page: int = Field(0, ge=0)
    event_id: Optional[int] = Field(None, gt=0)
    sensor_id: Optional[int] = Field(None, gt=0)
    temperature: Optional[float] = Field(None, gt=-100.0, lt=1500)
    humidity: Optional[float] = Field(None, ge=0, le=100)

    @field_validator("event_id")
    def check_exclusive(cls, v, info):
        exclude_fields = [info.data.get(field) for field in ("sensor_id", "temperature", "humidity")]
        if v and not all([field is None for field in exclude_fields]):
            raise ValueError("Нельзя указывать event_id одновременно c парамтерами фильтрации")
        return v


class Event(BaseModel):
    id: Optional[int] = Field(None, gt=0)
    sensor_id: int = Field(gt=0)
    name: str = Field(max_length=100)
    temperature: Optional[float] = Field(None, gt=-100.0, lt=1500)
    humidity: Optional[float] = Field(None, ge=0, le=100)

@events_router.get("/events/")
def get_event(filter_params: Annotated[FilterParams, Query()]):
    return {
        "event_id": filter_params.event_id, 
        "limit": filter_params.limit, 
        "page": filter_params.page,
        "sensor_id": filter_params.sensor_id,
        "temperature": filter_params.temperature,
        "humidity": filter_params.humidity,
    }

@events_router.post("/event/")
def post_event(event: Annotated[Event, Body(embed=True)]):
    # сохраняем ивент в базу, получаем его id
    event_id = 5
    return event_id

@events_router.put("/event/{event_id}")
def put_event(event_id: int, event: Annotated[Event, Body(embed=True)]):
    results = event
    return results

@events_router.delete("/event/{event_id}")
def delete_event(event_id: int, event: Annotated[Event, Body(embed=True)]):
    results = event
    return results
