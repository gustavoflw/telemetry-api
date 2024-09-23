import asyncio
from app.database import AsyncSessionLocal
from app.crud import create_device
from app.schemas import TelemetryDeviceCreate

sample_devices = [
    {"name": "Temperature Sensor A", "location": "Building 1", "data": 23.5},
    {"name": "Pressure Sensor B", "location": "Building 2", "data": 1.2},
    {"name": "Humidity Sensor C", "location": "Building 3", "data": 45.0},
]

async def populate_db():
    async with AsyncSessionLocal() as db:
        for device_data in sample_devices:
            device = TelemetryDeviceCreate(**device_data)
            await create_device(db, device)

if __name__ == "__main__":
    asyncio.run(populate_db())
