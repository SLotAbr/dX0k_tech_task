from fastapi import APIRouter
from .users import UsersRouter
from .orders import OrdersRouter


router = APIRouter()


router.include_router(
    UsersRouter, tags=["users"]
)
router.include_router(
    OrdersRouter, prefix="/orders", tags=["orders"]
)

