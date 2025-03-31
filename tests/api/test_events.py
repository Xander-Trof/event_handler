import pytest
from sqlalchemy import and_

from app.api.schema import MAX_HUM, MAX_TEMP, MIN_HUM, MIN_TEMP
from app.db.models import Event, Sensor


class TestEvents:
    def test_get_event_by_id(self, test_client, test_event):
        resp = test_client.get(f"/event/{test_event.id}")

        assert resp.status_code == 200, resp.json()
        assert resp.json().get("event")["id"] == test_event.id

    @pytest.mark.parametrize(
        "limit, page, status_code, error_type",
        (
            (0, 0, 422, "greater_than"),
            (101, 0, 422, "less_than_equal"),
        ),
    )
    def test_get_events_wrong_pagination(
        self, limit, page, status_code, error_type, test_client
    ):
        resp = test_client.get(f"/events/?limit={limit}&page={page}")

        detail = resp.json().get("detail", [{}])

        assert resp.status_code == status_code
        assert detail[0].get("type") == error_type

    @pytest.mark.parametrize(
        "limit, page, events_count",
        (
            (1, 0, 1),
            (10, 0, 10),
            (5, 3, 5),
            (22, 4, 0),
        ),
    )
    def test_get_events_correct_pagination(
        self, limit, page, events_count, test_client, test_data
    ):
        resp = test_client.get(f"/events/?limit={limit}&page={page}")

        assert resp.status_code == 200
        assert len(resp.json().get("events")) == events_count
        assert resp.json().get("page") == page

    @pytest.mark.parametrize(
        "sensor_id",
        (
            500,
            3,
        ),
    )
    def test_get_events_by_sensor_id(self, sensor_id, test_client, test_data):
        resp = test_client.get(f"/events/?sensor_id={sensor_id}")

        expected_events = [
            event for event in test_data if event["sensor_id"] == sensor_id
        ]
        expected_len = len(expected_events)
        real_len = len(resp.json().get("events"))

        assert resp.status_code == 200
        assert (
            expected_len == real_len
        ), f"ожидали {expected_len}, а получили {real_len}"

    @pytest.mark.parametrize(
        "min_temp, max_temp",
        (
            (25, 25),
            (16, 23),
            (None, 23),
            (16, None),
        ),
    )
    def test_filter_events_by_temperature(
        self, min_temp, max_temp, test_client, test_data
    ):
        min_temp_str = f"min_temp={min_temp}" if min_temp else ""
        max_temp_str = f"max_temp={max_temp}" if max_temp else ""
        ampersand = "&" if min_temp and max_temp else ""

        resp = test_client.get(f"/events/?{min_temp_str}{ampersand}{max_temp_str}")
        real = resp.json().get("events")

        min_temp = min_temp or MIN_TEMP
        max_temp = max_temp or MAX_TEMP
        expected = [
            instance
            for instance in test_data
            if min_temp <= instance.get("temperature", -500) <= max_temp
        ]

        assert resp.status_code == 200, resp.json()
        assert len(real) == len(
            expected
        ), f"ожидали {[x.get('temperature') for x in expected]}, получили {[x.get('temperature') for x in real]}"

    @pytest.mark.parametrize(
        "min_hum, max_hum", ((30, 50), (45, 45), (None, 50), (30, None))
    )
    def test_filter_events_by_humidity(self, min_hum, max_hum, test_client, test_data):
        min_hum_str = f"min_hum={min_hum}" if min_hum else ""
        max_hum_str = f"max_hum={max_hum}" if max_hum else ""
        ampersand = "&" if min_hum and max_hum else ""

        resp = test_client.get(f"/events/?{min_hum_str}{ampersand}{max_hum_str}")
        real = resp.json().get("events")

        min_hum = min_hum or MIN_HUM
        max_hum = max_hum or MAX_HUM
        expected = [
            instance
            for instance in test_data
            if min_hum <= instance.get("humidity", -1) <= max_hum
        ]

        assert resp.status_code == 200, resp.json()
        assert len(real) == len(
            expected
        ), f"ожидали {[x.get('humidity') for x in expected]}, получили {[x.get('humidity') for x in real]}"

    @pytest.mark.parametrize(
        "temperature, humidity",
        (
            (-271, 30),
            (0, 101),
        ),
    )
    def test_post_incorrect_event(self, temperature, humidity, test_client, db_session):
        data = {
            "sensor_id": 1,
            "name": "test event",
            "temperature": temperature,
            "humidity": humidity,
        }

        resp = test_client.post("/event/", json=data)

        incorrect_events = (
            db_session.query(Event)
            .filter(
                and_(
                    Event.temperature == temperature,
                    Event.humidity == humidity,
                    Event.sensor_id == data["sensor_id"],
                    Event.name == data["name"],
                )
            )
            .all()
        )

        assert resp.status_code == 422
        assert incorrect_events == []

    def test_post_correct_event(self, test_client, db_session):
        db_session.query(Event).delete()
        db_session.query(Sensor).delete()
        db_session.commit()

        data = {
            "sensor_id": 1,
            "name": "test event",
            "temperature": 25,
            "humidity": 50,
        }

        resp = test_client.post("/event/", json=data)

        correct_event = db_session.get(Event, resp.json().get("event_id"))
        sensor = db_session.get(Sensor, data["sensor_id"])

        assert resp.status_code == 200, resp.json()
        assert correct_event.sensor_id == data["sensor_id"]
        assert correct_event.name == data["name"]
        assert correct_event.temperature == data["temperature"]
        assert correct_event.humidity == data["humidity"]
        assert correct_event.sensor == sensor

    def test_put_event(self, test_client, db_session, test_event):
        data = {
            "sensor_id": 1,
            "name": "test event",
            "temperature": 25,
            "humidity": 50,
        }

        resp = test_client.put(f"/event/{test_event.id}", json=data)

        db_session.expire_all()
        changed_event = db_session.get(Event, test_event.id)

        assert resp.status_code == 200, resp.json()
        assert changed_event.temperature == data["temperature"], (
            changed_event,
            test_event,
        )
        assert changed_event.humidity == data["humidity"]

    def test_delete_event(self, test_client, test_event, db_session):
        resp = test_client.delete(f"/event/{test_event.id}")
        deleted_event = db_session.query(Event).filter(Event.id == test_event.id).all()

        assert resp.status_code == 200, resp.json()
        assert deleted_event == [], deleted_event
