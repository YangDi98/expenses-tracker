from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String

from src.models.base import SoftDeleteModel, CreateUpdateModel
from src.extensions import db
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.models.expenses import Expense


class Category(SoftDeleteModel, CreateUpdateModel):
    __tablename__ = "categories"
    __tableargs__ = db.Index("idx_category_name", "name")
    name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    description: Mapped[str] = mapped_column(String(255), nullable=True)
    color: Mapped[str] = mapped_column(
        String(7), nullable=True
    )  # e.g., Hex color code
    expenses: Mapped[list["Expense"]] = relationship(back_populates="category")
