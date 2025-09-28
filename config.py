import os
from typing import Dict

# Database configurations for 4 separate databases
DATABASE_CONFIGS: Dict[str, str] = {
    "student": "postgresql://postgres:tara@localhost:5432/school_students",
    "teacher": "postgresql://postgres:tara@localhost:5432/school_teachers", 
    "authority": "postgresql://postgres:tara@localhost:5432/school_authority",
    "public": "postgresql://postgres:tara@localhost:5432/school_public"
}

# Security settings
SECRET_KEY = "your-secret-key-change-this-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# App settings
APP_NAME = "School Management Portal"
DEBUG = True