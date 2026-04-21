import pytest
from time import time, sleep
from httpx import AsyncClient
from tests.utils import (
    _enable_security_header, 
    create_fake_order, 
    is_valid_uuid, 
    is_valid_datetime
)


@pytest.mark.asyncio
async def test_register_orders(client: AsyncClient) -> None:
    await _enable_security_header(client)
    
    # invalid values
    wrong_uuid = create_fake_order({"item_uuid":""})
    response = await client.post("/orders/", json={"items": [wrong_uuid]})
    assert response.status_code == 422
    assert response.json()["detail"] is not None
    
    wrong_price = create_fake_order({"price":-100})
    response = await client.post("/orders/", json={"items": [wrong_price]})
    assert response.status_code == 422
    assert response.json()["detail"] is not None
    
    wrong_amount = create_fake_order({"amount":-10})
    response = await client.post("/orders/", json={"items": [wrong_amount]})
    assert response.status_code == 422
    assert response.json()["detail"] is not None
    # duplicate items
    item = create_fake_order()
    payload = {"items": [item, item]}
    assert response.status_code == 422
    assert response.json()["detail"] is not None
    ## valid input
    payload = {"items": [create_fake_order(), create_fake_order()]}
    response = await client.post("/orders/", json=payload)
    assert response.status_code == 201
    assert is_valid_uuid(response.json()["id"])
    assert response.json()["user_id"] == 1
    assert response.json()["items"] == payload["items"]
    assert isinstance(response.json()["total_price"], float)
    assert response.json()["status"] == "pending"
    assert is_valid_datetime(response.json()["created_at"])


@pytest.mark.asyncio
async def test_get_orders(client: AsyncClient) -> None:
    await _enable_security_header(client)
    
    # GET 1 order
    response = await client.post("/orders/", json={"items": [create_fake_order()]})
    response = await client.get(f"/orders/{response.json()['id']}")
    assert response.status_code == 200
    # GET several orders
    response = await client.post("/orders/", json={"items": [create_fake_order()]})
    response = await client.get(f"/orders/user/1")
    assert response.status_code == 200
    assert len(response.json()) == 2
    # GET orders of another user
    await _enable_security_header(client)
    response = await client.post("/orders/", json={"items": [create_fake_order()]})
    response = await client.get(f"/orders/user/2")
    assert response.status_code == 200
    assert len(response.json()) == 1


@pytest.mark.asyncio
async def test_patch_order_status(client: AsyncClient) -> None:
    await _enable_security_header(client)
    
    response = await client.post("/orders/", json={"items": [create_fake_order()]})
    assert response.json()["status"] == "pending"
    order_uuid = response.json()["id"]
    # Event loop is closed?
    response = await client.patch(f"/orders/{order_uuid}", json={"status": "wrong_status"})
    assert response.status_code == 422
    assert response.json()["detail"] is not None
    
    for status in ["paid", "shipped", "cancelled"]:
        response = await client.patch(
            f"/orders/{order_uuid}", json={"status": status}
        )
        assert response.status_code == 200
        assert response.json()["status"] == status


@pytest.mark.asyncio
async def test_orders_caching(client: AsyncClient) -> None:
    await _enable_security_header(client)
    
    response = await client.post("/orders/", json={"items": [create_fake_order()]})
    search_uuid = response.json()['id']
    # GET
    now = time()
    response = await client.get(f"/orders/{search_uuid}")
    duration0 = time() - now
    assert response.status_code == 200
    now = time()
    response = await client.get(f"/orders/{search_uuid}")
    duration1 = time() - now
    assert response.status_code == 200
    assert duration1 < duration0
    # PATCH
    status = "cancelled"
    response = await client.patch(f"/orders/{search_uuid}", json={"status": status})
    assert response.status_code == 200
    assert response.json()["status"] == status
    now = time()
    response = await client.get(f"/orders/{search_uuid}")
    duration2 = time() - now
    assert response.status_code == 200
    assert response.json()["status"] == status
    assert duration2 < duration0


























