import datetime
from fastapi import FastAPI, status
from backend import config
from starlette.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from logging.config import dictConfig
import logging
from backend.logger import LogConfig

from backend.auth.router import router as auth_router
from backend.users.router import router as users_router
from backend.items.router import router as items_router

dictConfig(LogConfig().model_dump())

logger = logging.getLogger(f"{config.SERVICE_NAME}_logger")


app = FastAPI(
    title=f"{config.SERVICE_NAME} API",
    description=f"API for the {config.SERVICE_NAME} project",
    version="0.0.1",
    contact={},
    openapi_url=config.OPENAPI_URL if config.DEBUG else None,
    docs_url=config.DOCS_URL if config.DEBUG else None,
    redoc_url=config.REDOC_URL if config.DEBUG else None,
    debug=config.DEBUG
)


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse({"detail": [{"msg": exc.detail, "loc": [], "type": "error"}]}, status_code=exc.status_code)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True if config.DEBUG else False,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)


app.include_router(auth_router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(users_router, prefix="/api/v1/users", tags=["users"])
app.include_router(items_router, prefix="/api/v1/items", tags=["items"])

@app.on_event("startup")
async def startup_event():
   logger.debug('Server started')
   
@app.on_event("shutdown")
async def shutdown_event():
   logger.debug('Server shutdown')