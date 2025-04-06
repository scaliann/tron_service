from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class WalletLog(Base):
    __tablename__ = "wallet_logs"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    address: Mapped[str] = mapped_column(index=True)
    timestamp: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    balance: Mapped[float]
    energy: Mapped[float]
    bandwidth: Mapped[float]
