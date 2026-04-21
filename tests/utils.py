from httpx import AsyncClient
from uuid import UUID, uuid4
from datetime import datetime
import random
import string


def is_valid_uuid(value) -> bool:
    try:
        UUID(value)
        return True
    except:
        return False


def is_valid_datetime(value) -> bool:
    try:
        datetime.fromisoformat(value)
        return True
    except:
        return False


def generate_random_string(n) -> str:
    return ''.join(random.choices(string.ascii_letters, k=n))


def create_fake_order(extra: dict = {}) -> dict:
    fake_order = {
        "item_uuid": str(uuid4()),
        "price": random.normalvariate(1_000, 50),
        "amount": random.randint(1,5)
    }
    for key, value in extra.items():
        fake_order[key] = value
    return fake_order


async def _enable_security_header(client: AsyncClient) -> None:
    credentials = generate_random_string(10)
    fake_user = {
        "username": credentials,
        "email": credentials + "@example.com",
        "password": generate_random_string(10),
    }
    await client.post("/register", json=fake_user)
    response = await client.post("/token", data=fake_user)
    access_token = response.json()["access_token"]
    client.headers.update({"Authorization": f"Bearer {access_token}"})
    return None

