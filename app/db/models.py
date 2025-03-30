import enum

import sqlalchemy

from typing import List
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship


class Base(DeclarativeBase):
    pass


class Event(Base):
    __tablename__ = "event"

    id: Mapped[int] = mapped_column(sqlalchemy.Integer, primary_key=True)
    name: Mapped[str] = mapped_column(sqlalchemy.String(100))
    temperature: Mapped[float] = mapped_column(sqlalchemy.Float(), nullable=True)
    humidity: Mapped[float] = mapped_column(sqlalchemy.Float(), nullable=True)
    sensor_id: Mapped[int] = mapped_column(sqlalchemy.ForeignKey("sensor.id"))

    sensor: Mapped["Sensor"] = relationship(back_populates="events")

    __table_args__ = (
        sqlalchemy.CheckConstraint("temperature >-100 AND temperature <2000", name="check_temperature_range"),
        sqlalchemy.CheckConstraint("humidity >=0 AND humidity <=100", name="check_humidity_range"),
    )

    def __repr__(self) -> str:
        return f"Event(id={self.id}, name={self.name}, temperature={self.temperature}, humidity={self.humidity}, sensor_id={self.sensor_id})"


class SensorType(enum.Enum):
    ONE = 1
    TWO = 2
    THREE = 3


class Sensor(Base):
    __tablename__ = "sensor"

    id: Mapped[int] = mapped_column(sqlalchemy.Integer, primary_key=True)
    name: Mapped[str] = mapped_column(sqlalchemy.String(100))
    sensor_type: Mapped[SensorType] = mapped_column(sqlalchemy.Enum(SensorType))

    events: Mapped[List["Event"]] = relationship(back_populates="sensor", cascade="all, delete-orphan")

    def __repr__(self):
        return f"Sensor(id={self.id}, name={self.name}, sensor_type={self.sensor_type})"
