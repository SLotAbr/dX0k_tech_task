from uuid import UUID
from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_async_session
from src import schemas
from src.models import User, Order
from src.security import get_current_user
from src.cache import ObjectCacheHandler, CacheDecoratorFactory
from src.config import config
from worker import queue_order


OrdersRouter = APIRouter()


@CacheDecoratorFactory(ttl=config.REDIS_TIME_TO_LIVE_SECONDS)
async def get_order_or_404(
    order_uuid: UUID, 
    session: AsyncSession = Depends(get_async_session),
) -> Order:
    query = select(Order).where(Order.id == order_uuid)
    query = await session.scalars(query)
    order = query.one_or_none()
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Order with given uuid is not found"
        )
    return order


@OrdersRouter.post("/", status_code=status.HTTP_201_CREATED)
async def register_order(
    register_order: schemas.RegisterOrder, # list[Item]
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(get_current_user),
) -> schemas.ReadOrder:
    """Создание заказа на основе списка товаров. Для каждого товара необходимо 
    указание его UUID4 идентификатора (проходит валидацию, пример для удобства: 
    "386abd76-dc9b-457d-bc2e-65024488371e"), цены и заказываемого числа. После
    в базу данных поступит запись заказа с пользовательским id, общей ценой и
    датой. Запись сопровождается передачей сообщения брокеру RabbitMQ и через
    него Celery для фоновой обработки.
    """
    order = Order(
        user_id = user.id,
        # to convert UUID4 objects to str format
        items = register_order.model_dump(mode="json")["items"], 
        total_price = sum(
            item.price*item.amount for item in register_order.items
        ),
    )
    session.add(order)
    await session.commit()
    queue_order.delay(order.id)
    return order


@OrdersRouter.get("/{order_uuid}")
async def get_order(
    order: Order = Depends(get_order_or_404),
    user: User = Depends(get_current_user),
) -> schemas.ReadOrder:
    """Получение информации о заказе по его уникальному идентификатору. 
    Обращается к базе данных только в случае отсутствия записи в кеше.
    """
    return order


@OrdersRouter.get("/user/{user_id}")
async def get_user_orders(
    user_id: int,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(get_current_user),
) -> list[schemas.ReadOrder]:
    """Получение информации о заказах пользователя с данным user_id.
    """
    query = select(Order).where(Order.user_id == user_id)
    # # or "results = await session.scalars(query)"
    results = await session.execute(query)
    return results.scalars().all()


@OrdersRouter.patch("/{order_uuid}")
async def patch_order(
    order_uuid: UUID,
    patch_order_status: schemas.PatchOrder,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(get_current_user),
) -> schemas.ReadOrder:
    """Обновляет статус заказа с данным order_uuid. Обновляет запись о заказе в кеше.
    """
    order = await get_order_or_404(order_uuid=order_uuid, session=session)
    order.status = patch_order_status.status
    session.add(order)
    await session.commit()
    
    await ObjectCacheHandler.set(
        key=f"{get_order_or_404.__name__}:{order_uuid}", 
        value=order, 
        ttl=config.REDIS_TIME_TO_LIVE_SECONDS
    )
    return order

























