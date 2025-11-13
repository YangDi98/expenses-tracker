from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String
from flask_smorest import abort
from http import HTTPStatus

from src.models.base import SoftDeleteModel, CreateUpdateModel
from src.extensions import db
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.models.expenses import Expense
    from src.models.users import User


class Category(SoftDeleteModel, CreateUpdateModel):
    __tablename__ = "categories"
    __tableargs__ = db.Index("idx_category_name", "name")
    name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    user_id: Mapped[int] = mapped_column(
        db.ForeignKey("users.id", name="fk_category_user_id"),
        nullable=True,
    )
    description: Mapped[str] = mapped_column(String(255), nullable=True)
    color: Mapped[str] = mapped_column(
        String(7), nullable=True
    )  # e.g., Hex color code
    expenses: Mapped[list["Expense"]] = relationship(back_populates="category")
    user: Mapped["User"] = relationship(back_populates="categories")

    @classmethod
    def get_by_user_id_and_id_or_404(cls, user_id: int, id: int):
        stmt = cls.select_active().where(cls.id == id, cls.user_id == user_id)
        result = db.session.execute(stmt).scalars().first()
        if not result:
            abort(
                HTTPStatus.NOT_FOUND,
                message=f"Category with id {id} not found for user {user_id}",
            )
        return result
