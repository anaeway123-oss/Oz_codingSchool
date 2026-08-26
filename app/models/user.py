from datetime import datetime

from sqlalchemy import Boolean, DateTime, Enum, Integer, String, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db.databases import Base
from app.models.enums import Department, Gender, Role


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    email: Mapped[str | None] = mapped_column(String(255), unique=True)
    hashed_password: Mapped[str | None] = mapped_column(String(255))
    name: Mapped[str | None] = mapped_column(String(20))
    phone_number: Mapped[str | None] = mapped_column(String(20), unique=True)
    gender: Mapped[Gender] = mapped_column(Enum(Gender, name="gender"), nullable=False)
    department: Mapped[Department] = mapped_column(
        Enum(Department, name="department"), nullable=False
    )
    role: Mapped[Role] = mapped_column(Enum(Role, name="role"), nullable=False)
    is_active: Mapped[bool] = mapped_column(
        Boolean, nullable=False, server_default=text("true")
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP")
    )
    updated_at: Mapped[datetime | None] = mapped_column(DateTime)

    xray_images: Mapped[list["XrayImage"]] = relationship(back_populates="uploader")
