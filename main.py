from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

# Импортируем наш db_helper и модель
from core.models.db_helper import db_helper
from core.models.wallet_log import Base, WalletLog

app = FastAPI()

# Pydantic-модель для тела запроса
class WalletRequest(BaseModel):
    address: str

def get_wallet_info_dummy(address: str):
    return {
        "address": address,
        "bandwidth": "dummy_bandwidth",
        "energy": "dummy_energy",
        "balance_trx": "dummy_balance"
    }

@app.on_event("startup")
async def on_startup():
    """
    Создание таблиц в базе данных (если их нет).
    Для асинхронного движка используем run_sync.
    """
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.post("/wallet")
async def post_wallet(
    request: WalletRequest,
    db: AsyncSession = Depends(db_helper.session_dependency)
):
    # Получаем данные о кошельке (фиктивно)
    wallet_info = get_wallet_info_dummy(request.address)

    # Создаём запись в БД
    new_log = WalletLog(address=request.address)
    db.add(new_log)

    # В асинхронном режиме commit, refresh, delete и т.д. — тоже await
    await db.commit()
    await db.refresh(new_log)

    return wallet_info

@app.get("/logs")
async def get_logs(
    limit: int = 10,
    offset: int = 0,
    db: AsyncSession = Depends(db_helper.session_dependency)
):
    # Делаем асинхронный запрос через select
    result = await db.execute(
        select(WalletLog).offset(offset).limit(limit)
    )
    logs = result.scalars().all()
    return logs
