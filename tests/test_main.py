import pytest
import asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from app.database import get_db
from app.models import Base
from app.schemas import TelemetryDeviceCreate
from app.crud import create_device
from main import app

DATABASE_URL = "sqlite+aiosqlite:///./test.db"

engine = create_async_engine(DATABASE_URL, echo=True)
TestingSessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

@pytest.fixture
async def async_session():
    # Create the database schema
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    # Provide the session to the test
    async with TestingSessionLocal() as session:
        yield session
    # Drop the database schema after the test
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.fixture
async def client(async_session):
    # Override the get_db dependency to use the testing session
    async def override_get_db():
        yield async_session
    app.dependency_overrides[get_db] = override_get_db
    # Create an AsyncClient for testing
    async with AsyncClient(app=app, base_url="http://test") as c:
        yield c
    # Remove the override after the test
    app.dependency_overrides.clear()

@pytest.mark.asyncio
async def test_create_device(client):
    response = await client.post("/telemetry/", json={
        "name": "Test Device",
        "location": "Test Location",
        "data": 42.0
    })
    assert response.status_code == 201
    assert response.json()["name"] == "Test Device"

@pytest.mark.asyncio
async def test_read_devices(client, async_session):
    # Create sample data
    device_data = {
        "name": "Device 1",
        "location": "Location 1",
        "data": 12.34
    }
    device = TelemetryDeviceCreate(**device_data)
    await create_device(async_session, device)
    await async_session.commit()

    response = await client.get("/telemetry/")
    assert response.status_code == 200
    assert len(response.json()) >= 1
    assert response.json()[0]["name"] == device_data["name"]

@pytest.mark.asyncio
async def test_read_device(client, async_session):
    # Create sample data
    device_data = {
        "name": "Device 2",
        "location": "Location 2",
        "data": 56.78
    }
    device = TelemetryDeviceCreate(**device_data)
    created_device = await create_device(async_session, device)
    await async_session.commit()

    response = await client.get(f"/telemetry/{created_device.id}")
    assert response.status_code == 200
    assert response.json()["id"] == created_device.id
    assert response.json()["name"] == device_data["name"]

@pytest.mark.asyncio
async def test_update_device(client, async_session):
    # Create sample data
    device_data = {
        "name": "Device 3",
        "location": "Location 3",
        "data": 90.12
    }
    device = TelemetryDeviceCreate(**device_data)
    created_device = await create_device(async_session, device)
    await async_session.commit()

    # Update the device
    updated_data = {
        "name": "Updated Device 3",
        "location": "Updated Location 3",
        "data": 100.0
    }
    response = await client.put(f"/telemetry/{created_device.id}", json=updated_data)
    assert response.status_code == 200
    assert response.json()["name"] == updated_data["name"]

@pytest.mark.asyncio
async def test_delete_device(client, async_session):
    # Create sample data
    device_data = {
        "name": "Device 4",
        "location": "Location 4",
        "data": 34.56
    }
    device = TelemetryDeviceCreate(**device_data)
    created_device = await create_device(async_session, device)
    await async_session.commit()

    # Delete the device
    response = await client.delete(f"/telemetry/{created_device.id}")
    assert response.status_code == 200

    # Verify deletion
    response = await client.get(f"/telemetry/{created_device.id}")
    assert response.status_code == 404
