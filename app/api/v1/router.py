from fastapi import APIRouter

from .customers import router as customer_router
from .films import router as film_router

api_v1_router = APIRouter(
    prefix="/api/v1"
)

api_v1_router.include_router(customer_router)
api_v1_router.include_router(film_router)