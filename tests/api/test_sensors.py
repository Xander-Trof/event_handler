from app.api.schema import SensorType
from app.db.models import Sensor


class TestSensors:
    def test_get_sensor_by_id(self, test_client, test_sensor):
        resp = test_client.get(f"/sensor/{test_sensor.id}")

        assert resp.status_code == 200, resp.json()
        assert resp.json().get("sensor")["id"] == test_sensor.id

    def test_post_incorrect_sensor(self, test_client, db_session):
        data = {
            "name": "test sensor",
            "type": 5,
        }

        resp = test_client.post("/sensor/", json=data)

        assert resp.status_code == 422

    def test_post_correct_sensor(self, test_client, db_session):
        data = {
            "name": "test sensor",
            "type": 2,
        }

        resp = test_client.post("/sensor/", json=data)

        correct_sensor = db_session.get(Sensor, resp.json().get("sensor_id"))

        assert resp.status_code == 200, resp.json()
        assert correct_sensor is not None

    def test_put_sensor(self, test_client, db_session, test_sensor):
        data = {
            "name": "test sensor 2",
            "type": SensorType.THREE.value,
        }

        resp = test_client.put(f"/sensor/{test_sensor.id}", json=data)

        db_session.expire_all()
        changed_sensor = db_session.get(Sensor, test_sensor.id)

        assert resp.status_code == 200, resp.json()
        assert (
            changed_sensor.name == data["name"]
        ), f"ожидали {data['name']}, получили {changed_sensor.name})"
        assert (
            changed_sensor.sensor_type == data["type"]
        ), f"ожидали {data['type']}, получили {changed_sensor.sensor_type})"

    def test_delete_sensor(self, test_client, test_sensor, db_session):
        resp = test_client.delete(f"/sensor/{test_sensor.id}")
        deleted_sensor = (
            db_session.query(Sensor).filter(Sensor.id == test_sensor.id).all()
        )

        assert resp.status_code == 200, resp.json()
        assert deleted_sensor == [], deleted_sensor
