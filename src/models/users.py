from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, or_

from src.models.base import SoftDeleteModel, CreateUpdateModel
from src.extensions import db, bcrypt
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from src.models.expenses import Expense
    from src.models.categories import Category


class User(SoftDeleteModel, CreateUpdateModel):
    __tablename__ = "users"
    __tableargs__ = db.Index("idx_user_username", "username")
    active: Mapped[bool] = mapped_column(
        nullable=False, default=True, server_default="1"
    )
    username: Mapped[str] = mapped_column(
        String(50), nullable=False, unique=True
    )
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(
        String(100), nullable=False, unique=True
    )
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    expenses: Mapped[list["Expense"]] = relationship(back_populates="user")
    categories: Mapped[list["Category"]] = relationship(back_populates="user")

    @classmethod
    def get_by_username_or_email(cls, login: str):
        """Find user by username or email (case-insensitive)"""
        stmt = cls.select_active().where(
            or_(cls.username == login.lower(), cls.email == login.lower())
        )
        return db.session.execute(stmt).scalars().first()

    def set_password(self, password: str):
        hashed = bcrypt.generate_password_hash(password).decode("utf-8")
        self.password_hash = hashed
        self.save()
