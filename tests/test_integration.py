import pytest
from httpx import ASGITransport, AsyncClient
from main import app


@pytest.mark.asyncio
async def test_post_and_get_logs():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        wallet_payload = {"address": "T9yD14Nj9j7xAB4dbGeiX9h8unkKHxuWwb"}
        post_response = await client.post("/wallet", json=wallet_payload)
        assert post_response.status_code == 200
        data = post_response.json()
        assert "address" in data
        assert "balance_trx" in data
        get_response = await client.get("/logs?limit=10&offset=0")
        assert get_response.status_code == 200
        logs = get_response.json()
        assert isinstance(logs, list)
        assert any(entry["address"] == wallet_payload["address"] for entry in logs)
