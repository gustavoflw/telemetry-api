from pydantic import BaseModel, Field

class TelemetryDeviceBase(BaseModel):
    name: str = Field(..., example="Temperature Sensor A")
    location: str = Field(..., example="Building 1")
    data: float = Field(..., example=23.5)

class TelemetryDeviceCreate(TelemetryDeviceBase):
    pass

class TelemetryDevice(TelemetryDeviceBase):
    id: int

    class Config:
        orm_mode = True
