from fastapi import FastAPI
from app.routers import telemetry, views
from fastapi.staticfiles import StaticFiles
import os
import uvicorn
import logging

# Logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Include routers
app.include_router(views.router)
app.include_router(telemetry.router)

# Mount static files
dir_path = os.path.dirname(os.path.realpath(__file__))
dir_static = os.path.join(dir_path, "app", "static")
app.mount("/static", StaticFiles(directory=dir_static), name="static")
