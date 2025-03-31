import json
import os

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.models import Base, Event, Sensor, SensorType
from app.main import app


@pytest.fixture()
def db_session():
    engine = create_engine(
        "postgresql+psycopg2://event_handler:111111@localhost:5432/postgres"
    )
    session_maker = sessionmaker(bind=engine)
    session = session_maker()

    yield session

    session.close()


@pytest.fixture()
def test_client():
    return TestClient(app)


@pytest.fixture()
def test_event(db_session):
    db_session.query(Event).delete()
    db_session.query(Sensor).delete()
    db_session.commit()
    event = Event(sensor_id=1, name="N/A", temperature=20, humidity=25)
    db_session.add(event)
    db_session.add(Sensor(id=1))
    db_session.commit()

    yield event


@pytest.fixture()
def test_sensor(db_session):
    db_session.query(Event).delete()
    db_session.query(Sensor).delete()
    db_session.commit()
    sensor = Sensor(name="test")
    db_session.add(sensor)
    db_session.commit()

    yield sensor


@pytest.fixture()
def test_data(db_session):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    test_data_file = os.path.join(current_dir, "events.json")
    with open(test_data_file, "r") as f:
        test_data = json.load(f)

    with db_session.begin():
        for table in reversed(Base.metadata.sorted_tables):
            db_session.execute(table.delete())

    sensor_ids = {event["sensor_id"] for event in test_data}
    items = [Sensor(id=id, name="N/A", sensor_type=SensorType(1)) for id in sensor_ids]
    items.extend(Event(**data) for data in test_data)

    db_session.add_all(items)
    db_session.commit()

    yield test_data
