from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import DateTime, Integer, func, select
from flask_smorest import abort
from datetime import datetime, timezone
from http import HTTPStatus

from src.extensions import db


class BaseModel(db.Model):
    __abstract__ = True
    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    @classmethod
    def get_by_id(cls, id: int):
        return (
            db.session.execute(select(cls).where(cls.id == id))
            .scalars()
            .first()
        )

    @classmethod
    def get_by_id_or_404(cls, id: int):
        result = cls.get_by_id(id)
        if not result:
            abort(HTTPStatus.NOT_FOUND, message="item not found")
        return result

    @classmethod
    def create(cls, data: dict, commit: bool = True, **kwargs):
        instance = cls(**data, **kwargs)
        db.session.add(instance)
        if commit:
            db.session.commit()
        return instance

    def save(self, commit: bool = False):
        db.session.add(self)
        if commit:
            db.session.commit()
        return self

    def update(self, data: dict, commit: bool = False):
        for key, value in data.items():
            setattr(self, key, value)
        if commit:
            db.session.commit()
        return self


class CreateUpdateModel(BaseModel):
    __abstract__ = True
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.now(timezone.utc),
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.now(timezone.utc),
        server_default=func.now(),
        onupdate=datetime.now(timezone.utc),
    )


class SoftDeleteModel(BaseModel):
    __abstract__ = True
    deleted_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)

    @classmethod
    def select_active(cls):
        return select(cls).where(cls.deleted_at.is_(None))

    @classmethod
    def select_with_deleted(cls):
        return select(cls)

    @classmethod
    def get_by_id(cls, id: int):
        stmt = cls.select_active().where(cls.id == id)
        return db.session.execute(stmt).scalars().first()

    @classmethod
    def get_by_id_or_404(cls, id: int):
        result = cls.get_by_id(id)
        if not result:
            abort(HTTPStatus.NOT_FOUND, message="item not found")
        return result

    def soft_delete(self, commit: bool = False):
        self.deleted_at = datetime.now(timezone.utc)
        if commit:
            db.session.commit()
        return self
