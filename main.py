from contextlib import asynccontextmanager
import json
from fastapi import FastAPI, Depends
from pydantic import BaseModel
from redis.asyncio import from_url
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy import select
import uvicorn
import redis
from core.models.db_helper import db_helper
from core.models.wallet_log import Base, WalletLog
from core.tron_tools import get_wallet_info

from schemas import WalletRequest

import logging

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(lifespan=lifespan)
redis_client = from_url("redis://redis:6379", decode_responses=True)


@app.post("/wallet", summary="Получить информацию о кошельке")
async def post_wallet(
    request: WalletRequest,
    session: AsyncSession = Depends(db_helper.session_dependency)
):
    try:
        cache_key = f"wallet:{request.address}"
        cached_wallet_info = await redis_client.get(cache_key)
        if cached_wallet_info:
            return json.loads(cached_wallet_info)
        wallet_info = await get_wallet_info(request.address)
        await redis_client.set(cache_key, json.dumps(wallet_info, default=float), ex=600)
        new_log = WalletLog(address=wallet_info['address'], balance=wallet_info['balance_trx'], energy=wallet_info['energy'], bandwidth=wallet_info['bandwidth'])
        session.add(new_log)
        await session.commit()
        await session.refresh(new_log)
        return wallet_info
    except Exception as e:
        logger.exception("Ошибка в эндпоинте /wallet:")
        raise e


@app.get("/logs", summary="Получить список последних запросов")
async def get_logs(
    limit: int = 10,
    session: AsyncSession = Depends(db_helper.session_dependency)
):
    result = await session.execute(
        select(WalletLog).order_by(WalletLog.timestamp.desc()).limit(limit)
    )
    logs = result.scalars().all()
    return logs


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0")
