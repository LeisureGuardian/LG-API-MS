from pydantic import BaseModel, Field


class DeviceStatusSchema(BaseModel):
    id: int = Field(default=None)
    deviceSerial: int = Field(...)
    longitude: float = Field(...)
    latitude: float = Field(...)
    temp: float = Field(...)
    accelMax: float = Field(...)
    heartRate: int = Field(...)
    batteryLevel: int = Field(...)
    critical: int = Field(...)
    button: int = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "deviceSerial": "1",
                "longitude": "128.39457",
                "latitude": "36.14199",
                "temp": "36.5",
                "accelMax": "0.5",
                "heartRate": "80",
                "batteryLevel": "50",
                "critical": "0",
                "button": "0"
            }
        }
