from fastapi.concurrency import run_in_threadpool
from tronpy import Tron
from tronpy.providers import HTTPProvider
from tronpy.exceptions import AddressNotFound

def _get_wallet_info(address: str) -> dict:
    client = Tron(HTTPProvider(api_key="84a49df2-018b-49ac-906f-a580a15ef330"))
    try:
        resource = client.get_account_resource(address)
        balance = client.get_account_balance(address)

        net_limit = resource.get("NetLimit", 0)
        net_used = resource.get("NetUsed", 0)
        bandwidth = net_limit - net_used

        energy_limit = resource.get("EnergyLimit", 0)
        energy_used = resource.get("EnergyUsed", 0)
        energy = energy_limit - energy_used

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
