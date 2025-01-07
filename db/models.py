import datetime
import enum
from sqlalchemy import create_engine, Column, String, Float, DateTime, Enum, Index
from sqlalchemy.orm import Mapped, mapped_column
from typing import Annotated
from uuid import uuid4, UUID

from db.database import Base

intpk = Annotated[int, mapped_column(primary_key=True)]


class SolanaSQLAlchemy(Base):
    __tablename__ = "solana"

    id: Mapped[intpk]
    price: Mapped[float] = mapped_column(Float, nullable=False)
    open: Mapped[float] = mapped_column(Float, nullable=False)
    close: Mapped[float] = mapped_column(Float, nullable=False)
    low: Mapped[float] = mapped_column(Float, nullable=False)
    high: Mapped[float] = mapped_column(Float, nullable=False)
    volume: Mapped[float] = mapped_column(Float, nullable=False)

    time: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    # Добавляем индекс на поле created_at
    __table_args__ = (
        Index('idx_time', 'time'),  # Имя индекса и колонка
    )
    """
        Что происходит с индексом?
            Индекс — это специальная структура данных, аналогичная сортированному указателю на строки таблицы.
            Когда добавляется индекс на поле created_at, база данных строит B-дерево или хэш-таблицу для быстрого поиска.
            При запросе база данных ищет не в основной таблице, а в индексе (как по оглавлению в книге).
            Это позволяет найти нужные строки за миллисекунды, независимо от размера таблицы.
    """

