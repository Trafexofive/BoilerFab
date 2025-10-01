"""
Configuration settings for the FastAPI Template Service
"""
import os
import json
from typing import List


class Settings:
    service_name = os.getenv("SERVICE_NAME", "FastAPI Template Service")
    service_host = os.getenv("SERVICE_HOST", "0.0.0.0")
    service_port = int(os.getenv("SERVICE_PORT", "8000"))
    debug_mode = os.getenv("DEBUG_MODE", "false").lower() == "true"
    log_level = os.getenv("LOG_LEVEL", "INFO")
    cors_origins = json.loads(os.getenv("CORS_ORIGINS", '["*"]'))
    templates_dir = os.getenv("TEMPLATES_DIR", "./templates")


settings = Settings()