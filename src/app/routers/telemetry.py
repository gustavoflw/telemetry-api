from fastapi import APIRouter, Depends, HTTPException, status
from .. import schemas, crud
from ..database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
import logging
from typing import List

router = APIRouter(
    prefix="/telemetry",
    tags=["telemetry"],
)

logger = logging.getLogger("uvicorn.error")

@router.get("/", response_model=List[schemas.TelemetryDevice])
async def read_devices(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    devices = await crud.get_devices(db, skip=skip, limit=limit)
    return devices

@router.post("/", response_model=schemas.TelemetryDevice, status_code=status.HTTP_201_CREATED)
async def create_device(device: schemas.TelemetryDeviceCreate, db: AsyncSession = Depends(get_db)):
    try:
        return await crud.create_device(db=db, device=device)
    except Exception as e:
        logger.error(f"Error creating device: {e}")
        raise HTTPException(status_code=400, detail="Error creating device")

@router.get("/{device_id}", response_model=schemas.TelemetryDevice)
async def read_device(device_id: int, db: AsyncSession = Depends(get_db)):
    device = await crud.get_device(db, device_id=device_id)
    if device is None:
        raise HTTPException(status_code=404, detail="Device not found")
    return device

@router.put("/{device_id}", response_model=schemas.TelemetryDevice)
async def update_device(device_id: int, device: schemas.TelemetryDeviceCreate, db: AsyncSession = Depends(get_db)):
    db_device = await crud.update_device(db, device_id=device_id, device=device)
    if db_device is None:
        raise HTTPException(status_code=404, detail="Device not found")
    return db_device

@router.delete("/{device_id}", response_model=schemas.TelemetryDevice)
async def delete_device(device_id: int, db: AsyncSession = Depends(get_db)):
    db_device = await crud.delete_device(db, device_id=device_id)
    if db_device is None:
        raise HTTPException(status_code=404, detail="Device not found")
    return db_device
