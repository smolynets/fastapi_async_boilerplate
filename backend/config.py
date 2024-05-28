import os
from dotenv import load_dotenv

load_dotenv()

SERVICE_NAME = os.getenv("SERVICE_NAME", "fastapi_boilerplate")

DEBUG = bool(int(os.getenv("DEBUG", "0")))
OPENAPI_URL = os.getenv("OPENAPI_URL", "/openapi.json")
DOCS_URL = os.getenv("DOCS_URL", "/docs")
REDOC_URL = os.getenv("REDOC_URL", "/redoc")

POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_USER = os.getenv("POSTGRES_USER", "psql_user")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "psql_password")
DATABASE = os.getenv("DATABASE", "psql_db")

