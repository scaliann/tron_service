import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


import pytest
from httpx import ASGITransport, AsyncClient
from main import app
@pytest.mark.asyncio


async def test_post_and_get_logs():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # Отправляем POST-запрос на эндпоинт /wallet
        wallet_payload = {"address": "T9yD14Nj9j7xAB4dbGeiX9h8unkKHxuWwb"}
        post_response = await client.post("/wallet", json=wallet_payload)
        assert post_response.status_code == 200
        data = post_response.json()
        assert "address" in data
        assert "balance_trx" in data

        # Отправляем GET-запрос на эндпоинт /logs с пагинацией
        get_response = await client.get("/logs?limit=10&offset=0")
        assert get_response.status_code == 200
        logs = get_response.json()
        assert isinstance(logs, list)
        # Проверяем, что в списке логов есть запись с нашим адресом
        assert any(entry["address"] == wallet_payload["address"] for entry in logs)
