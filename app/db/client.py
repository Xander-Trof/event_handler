from typing import List
from sqlalchemy import create_engine, and_
from sqlalchemy.orm import sessionmaker
from .models import Base, Event, Sensor
from app.api.schema import  FilterEventsParams, EventParams, SensorParams, SensorType


class Client:
    def __init__(self):
        self._engine = create_engine("postgresql+psycopg2://event_handler:111111@localhost:5432/postgres")
        self._session_maker = sessionmaker(bind=self._engine)
        self._session = self._session_maker()
        self._init_db()

    def _init_db(self):
        Base.metadata.create_all(bind=self._engine)

    def get_event_by_id(self, id: int):
        return self._session.get(Event, id)

    def update_event_by_id(self, event_id: int, event: EventParams):
        self._session.query(Event).filter(Event.id == event_id).update(
            {
                Event.sensor_id: event.sensor_id,
                Event.name: event.name,
                Event.temperature: event.temperature,
                Event.humidity: event.humidity,
            }
        )
        self._session.commit()
        return self.get_event_by_id(event_id)
    
    def create_event(self, event: EventParams):
        sensor = self._session.get(Sensor, event.sensor_id)
        if not sensor:
            self._session.add(Sensor(id=event.sensor_id))
        event = Event(**event.model_dump())
        self._session.add(event)
        self._session.commit()
        self._session.refresh(event)
        return event
    
    def delete_event(self, id: int):
        self._session.query(Event).filter(Event.id == id).delete()
        self._session.commit()
    
    def get_filtered_events(self, params: FilterEventsParams):

        query = self._session.query(Event)

        if not (params.max_temp == params.min_temp == None):
            if params.max_temp is not None:
                query = query.filter(Event.temperature <= params.max_temp)
            if params.min_temp is not None:
                query = query.filter(Event.temperature >= params.min_temp)
        
        if not (params.max_hum == params.min_hum == None):
            if params.max_hum is not None:
                query = query.filter(Event.humidity <= params.max_hum)
            if params.min_hum is not None:
                query = query.filter(Event.humidity >= params.min_hum)
        
        if params.sensor_id is not None:
            query = query.filter(Event.sensor_id == params.sensor_id)

        events = query.offset(params.page * params.limit)\
                 .limit(params.limit)\
                 .all()
        
        return events
    
    def create_multiple_events(self, events: List[EventParams]):
        events = [Event(**event) for event in events]

        sensor_ids = {event.sensor_id for event in events}
        existing_sensors = self._session.query(Sensor).filter(Sensor.id.in_(sensor_ids))
        existing_sensors_ids = {sensor.id for sensor in existing_sensors}
        need_to_create_sensors_ids = sensor_ids - existing_sensors_ids

        if len(need_to_create_sensors_ids) > 0:
            sensors = []
            for sensor_id in need_to_create_sensors_ids:
                sensors.append(Sensor(id=sensor_id))
            self._session.add_all(sensors)

        self._session.add_all(events)
        self._session.commit()

        for event in events:
            self._session.refresh(event)
        return events

    def get_sensor_by_id(self, id: int):
        return self._session.get(Sensor, id)
    
    def create_sensor(self, sensor: SensorParams):
        sensor = Sensor(name=sensor.name, sensor_type=SensorType(sensor.type))
        self._session.add(sensor)
        self._session.commit()
        self._session.refresh(sensor)
        return sensor
    
    def update_sensor_by_id(self, sensor_id: int, sensor: SensorParams):
        sensor_id = self._session.query(Sensor).filter(Sensor.id == sensor_id).update(
            {
                Sensor.sensor_type: SensorType(sensor.type),
                Sensor.name: sensor.name,
            }
        )
        self._session.commit()
        return sensor_id
    
    def delete_sensor(self, id: int):
        self._session.query(Sensor).filter(Sensor.id == id).delete()
        self._session.commit()

db_client = Client()