from uuid import uuid4
from datetime import datetime
from src.schemas import OrderStatus
from sqlalchemy import (
    ForeignKey, JSON, Integer, Float, Boolean, Unicode, UUID, DateTime, func, Enum
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    username: Mapped[str] = mapped_column(Unicode(255), nullable=False, unique=True)
    email: Mapped[str] = mapped_column(Unicode(255), nullable=False, unique=True)
    hashed_password: Mapped[str] = mapped_column(Unicode(255), nullable=False)
    disabled: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=func.now(), 
        nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, 
        default=func.now(), 
        onupdate=func.now(), 
        nullable=False
    )
    # one2many
    orders: Mapped[list["Order"]] = relationship(back_populates="user", passive_deletes=True)


class Order(Base):
    __tablename__ = "orders"
    
    id: Mapped[str] = mapped_column(
        UUID, default=uuid4, primary_key=True, unique=True, nullable=False
    )
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    user: Mapped["User"] = relationship(back_populates="orders")
    
    items: Mapped[list[dict]] = mapped_column(JSON, nullable=False)
    total_price: Mapped[float] = mapped_column(Float, nullable=False)
    status: Mapped[OrderStatus] = mapped_column(Enum(OrderStatus), default=OrderStatus.PENDING)
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=func.now(), 
        nullable=False
    )


























