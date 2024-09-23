from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from . import models, schemas
from typing import List

async def get_device(db: AsyncSession, device_id: int):
    result = await db.execute(
        select(models.TelemetryDevice).where(models.TelemetryDevice.id == device_id)
    )
    return result.scalar_one_or_none()

async def get_devices(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[models.TelemetryDevice]:
    result = await db.execute(select(models.TelemetryDevice).offset(skip).limit(limit))
    return result.scalars().all()

async def create_device(db: AsyncSession, device: schemas.TelemetryDeviceCreate):
    db_device = models.TelemetryDevice(**device.dict())
    db.add(db_device)
    await db.commit()
    await db.refresh(db_device)
    return db_device

async def update_device(db: AsyncSession, device_id: int, device: schemas.TelemetryDeviceCreate):
    db_device = await get_device(db, device_id)
    if db_device:
        for key, value in device.dict().items():
            setattr(db_device, key, value)
        await db.commit()
        await db.refresh(db_device)
    return db_device

async def delete_device(db: AsyncSession, device_id: int):
    db_device = await get_device(db, device_id)
    if db_device:
        await db.delete(db_device)
        await db.commit()
    return db_device
