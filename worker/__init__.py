import time
from uuid import UUID
from celery import Celery
from src.config import config


celery_app = Celery(
    broker=config.CELERY_BROKER_URL
)


@celery_app.task
def queue_order(order_id: UUID):
    time.sleep(2)
    print(f"Order {order_id} processed")

