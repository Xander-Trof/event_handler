import json
from typing import Annotated

from fastapi import APIRouter, Body, File, HTTPException, Query, UploadFile

from app.db.client import db_client

from .schema import EventParams, FilterEventsParams

events_router = APIRouter()


@events_router.get("/event/{event_id}")
def get_event_by_id(event_id: int):
    return {
        "event": db_client.get_event_by_id(event_id),
    }


@events_router.get("/events/")
def get_multiple_events(filter_params: Annotated[FilterEventsParams, Query()]):
    return {
        "events": db_client.get_filtered_events(filter_params),
        "page": filter_params.page,
    }


@events_router.post("/event/")
def post_event(event: Annotated[EventParams, Body(embed=False)]):
    event = db_client.create_event(event)
    return {"event_id": event.id}


@events_router.put("/event/{event_id}")
def put_event(event_id: int, event: Annotated[EventParams, Body(embed=False)]):
    return {"event": db_client.update_event_by_id(event_id, event)}


@events_router.delete("/event/{event_id}")
def delete_event(event_id: int):
    db_client.delete_event(event_id)
    return


@events_router.post("/event/file/")
async def save_json_file(file: Annotated[UploadFile, File()]):
    if file.content_type != "application/json":
        raise HTTPException(400, detail="Принимаются файлы только типа json")

    try:
        file_content = await file.read()
        data = json.loads(file_content)
    except json.JSONDecodeError as err:
        raise HTTPException(400, detail="Ошибка форматирования json файла")

    events = db_client.create_multiple_events(data)

    return {"events": events}
