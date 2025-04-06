from datetime import datetime, timezone
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class WalletLog(Base):
    __tablename__ = "wallet_logs"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    address: Mapped[str] = mapped_column(index=True)
    timestamp: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))
    balance: Mapped[float] = mapped_column(nullable=False, default=0.0, server_default="0")
    energy: Mapped[float] = mapped_column(nullable=False, default=0.0, server_default="0")
    bandwidth: Mapped[float] = mapped_column(nullable=False, default=0.0, server_default="0")
