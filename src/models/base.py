import datetime

from sqlalchemy.orm import DeclarativeBase, mapped_column
from sqlalchemy.sql.sqltypes import DateTime


class Base(DeclarativeBase):
    __abstract__ = True

    created_at = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.datetime.now(datetime.UTC),
    )

    updated_at = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.datetime.now(datetime.UTC),
        onupdate=lambda: datetime.datetime.now(datetime.UTC),
    )
