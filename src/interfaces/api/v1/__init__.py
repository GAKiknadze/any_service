from fastapi import APIRouter

from .routers import auth_router, session_router

v1_router = APIRouter()

# Routers initialization
v1_router.include_router(auth_router, prefix="/auth", tags=["auth"])
v1_router.include_router(session_router, prefix="/session", tags=["auth"])
