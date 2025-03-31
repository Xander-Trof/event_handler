import enum

from typing import Optional
from pydantic import BaseModel, Field, model_validator


MAX_TEMP = 2000
MIN_TEMP = -100
MAX_HUM = 100
MIN_HUM = 0


class FilterEventsParams(BaseModel):
    limit: int = Field(10, gt=0, le=100) 
    page: int = Field(0, ge=0)
    sensor_id: Optional[int] = Field(None, gt=0)
    min_temp: Optional[float] = Field(None, gt=MIN_TEMP, lt=MAX_TEMP)
    max_temp: Optional[float] = Field(None, gt=MIN_TEMP, lt=MAX_TEMP)
    min_hum: Optional[float] = Field(None, ge=MIN_HUM, le=MAX_HUM)
    max_hum: Optional[float] = Field(None, ge=MIN_HUM, le=MAX_HUM)

    @model_validator(mode="after")
    def check_temperature_range(self):
        if not any(temp is None for temp in (self.min_temp, self.max_temp)):
            if self.min_temp > self.max_temp:
                raise ValueError("min_temp не может быть больше max_temp")
        
        if not any(hum is None for hum in (self.min_hum, self.max_hum)):
            if self.min_hum > self.max_hum:
                raise ValueError("min_hum не может быть больше max_hum")
        
        return self


class EventParams(BaseModel):
    sensor_id: int = Field(gt=0)
    name: str = Field(max_length=100)
    temperature: Optional[float] = Field(None, gt=-100.0, lt=1500)
    humidity: Optional[float] = Field(None, ge=0, le=100)



class SensorType(enum.IntEnum):
    ONE = 1
    TWO = 2
    THREE = 3



class SensorParams(BaseModel):
    name: str = Field(max_length=100)
    type: int = Field(ge=1, le=3)
