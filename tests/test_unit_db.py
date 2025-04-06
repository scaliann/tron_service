import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy import text
from core.models.wallet_log import Base, WalletLog
from datetime import datetime

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

@pytest_asyncio.fixture(scope="module")
async def test_engine():
    engine = create_async_engine(TEST_DATABASE_URL, echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    await engine.dispose()

@pytest_asyncio.fixture(scope="function")
async def db_session(test_engine) -> AsyncSession:
    async_session = async_sessionmaker(bind=test_engine, expire_on_commit=False)
    async with async_session() as session:
        yield session

@pytest.mark.asyncio
async def test_db_write(db_session: AsyncSession):
    # Создаем новую запись
    new_log = WalletLog(
        address="T9yD14Nj9j7xAB4dbGeiX9h8unkKHxuWwb",
        balance=100.0,
        energy=10.0,
        bandwidth=20.0,
        timestamp=datetime.now()  # или можно оставить значение по умолчанию
    )
    db_session.add(new_log)
    await db_session.commit()
    await db_session.refresh(new_log)

    # Проверяем, что запись корректно записана в базу
    result = await db_session.execute(
        text("SELECT address, balance, energy, bandwidth FROM wallet_logs WHERE id = :id"),
        {"id": new_log.id}
    )
    record = result.fetchone()
    assert record is not None
    assert record.address == "T9yD14Nj9j7xAB4dbGeiX9h8unkKHxuWwb"
    assert record.balance == 100.0
    assert record.energy == 10.0
    assert record.bandwidth == 20.0
