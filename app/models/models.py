from datetime import date, datetime

from sqlalchemy import String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base


class BloodCenter(Base):
    __tablename__ = "blood_centers"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(60), unique=True)
    state: Mapped[str] = mapped_column(String(30), unique=True)
    city: Mapped[str] = mapped_column(String(50), nullable=True)
    address: Mapped[str] = mapped_column(String(150))
    website: Mapped[str] = mapped_column(String(260))
    active: Mapped[bool] = mapped_column(Boolean, default=True)

    stocks: Mapped[list["BloodCenterStocks"]] = relationship(back_populates="center")


class BloodCenterStockItem(Base):
    __tablename__ = "stock_items"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    collected_at: Mapped[date] = mapped_column()
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now, onupdate=datetime.now
    )

    blood_center_id: Mapped[int] = mapped_column(ForeignKey("blood_centers.id"))
