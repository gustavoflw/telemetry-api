from os.path import dirname, join as path_join
from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from ..database import get_db
from ..crud import get_devices

dir_app = dirname(dirname(__file__))
router = APIRouter()

templates = Jinja2Templates(directory=path_join(dir_app, "templates"))

@router.get("/")
async def read_root(request: Request, db: AsyncSession = Depends(get_db)):
    devices = await get_devices(db)
    return templates.TemplateResponse("index.html", {"request": request, "devices": devices})
