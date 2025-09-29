from sqlalchemy import String, Float
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from typing import Optional
from sqlalchemy import and_, or_

from src.models.base import SoftDeleteModel, CreateUpdateModel
from src.extensions import db


class Expense(SoftDeleteModel, CreateUpdateModel):
    __tablename__ = "expenses"
    __tableargs__ = db.Index("idx_expense_created_at_id", "created_at", "id")
    amount: Mapped[float] = mapped_column(Float, nullable=False)
    note: Mapped[str] = mapped_column(String(255), nullable=True)

    @classmethod
    def filter(
        cls,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        limit: int = 100,
        cursor_created_at: Optional[datetime] = None,
        cursor_id: Optional[int] = None,
    ):
        stmt = cls.select_active()
        if cursor_created_at and cursor_id:
            stmt = stmt.where(
                or_(
                    Expense.created_at < cursor_created_at,
                    and_(
                        Expense.created_at == cursor_created_at,
                        Expense.id < cursor_id,
                    ),
                )
            )
        elif cursor_created_at:
            stmt = stmt.where(Expense.created_at < cursor_created_at)
        if start_date:
            stmt = stmt.where(Expense.created_at >= start_date)
        if end_date:
            stmt = stmt.where(Expense.created_at <= end_date)
        stmt = stmt.order_by(
            Expense.created_at.desc(), Expense.id.desc()
        ).limit(limit)
        return db.session.execute(stmt).scalars().all()
