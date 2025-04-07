import time
from fastapi.concurrency import run_in_threadpool
from tronpy import Tron
from tronpy.providers import HTTPProvider
from tronpy.exceptions import AddressNotFound
from core.config import TRON_API_KEY

def _get_wallet_info(address: str) -> dict:
    client = Tron(HTTPProvider(api_key=TRON_API_KEY))
    try:
        resource = client.get_account_resource(address)
        balance = client.get_account_balance(address)
        bandwidth = client.get_bandwidth(address)
        energy = resource.get("TotalEnergyWeight", 0)
        time.sleep(5)
        return {
            "address": address,
            "bandwidth": bandwidth,
            "energy": energy,
            "balance_trx": balance
        }
    except AddressNotFound:
        return {"error": "Account not found on-chain", "address": address}


async def get_wallet_info(address: str) -> dict:
    return await run_in_threadpool(_get_wallet_info, address)
