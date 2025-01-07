import logging
import os
import shutil
import json
import traceback
from typing import List, Type, Literal

from sqlalchemy import Integer, and_, cast, func, insert, inspect, or_, select, text, desc
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime, timedelta


from db.database import Base, async_engine, async_session_factory
from db.models import SolanaSQLAlchemy
from db.schemas import SolanaDTO


class AsyncORM:

    @staticmethod
    async def create_tables(flag: Literal['delete', 'restart']):
        if flag == "delete":
            async with async_engine.begin() as conn:
                await conn.run_sync(Base.metadata.drop_all)
                await conn.run_sync(Base.metadata.create_all)

        elif flag == "restart":
            async with async_engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)

        else:
            raise ValueError("Недопустимое значение аргумента")

    @staticmethod
    async def insert_list_to_db(list_class_sqlalchemy: List[SolanaSQLAlchemy]):
        try:
            async with async_session_factory() as session:
                session.add_all(list_class_sqlalchemy)
                await session.commit()

        except Exception as e:
            print(f"Ошибка при записи списка в бд: {e}")

    @staticmethod
    async def insert_to_db(class_sqlalchemy: List[SolanaSQLAlchemy]):
        try:
            async with async_session_factory() as session:
                session.add(class_sqlalchemy)
                await session.commit()
        except Exception as e:
            print(f"Ошибка при записи в бд: {e}")

    @staticmethod
    async def select_transaction() -> List[SolanaDTO]:
        async with async_session_factory() as session:
            query = (
                select(SolanaSQLAlchemy)
            )
            res = await session.execute(query)
            result_orm = res.scalars().all()
            result_dto = [SolanaDTO.model_validate(row, from_attributes=True) for row in result_orm]
            return result_dto

    @staticmethod
    def json_to_dto(solana_dict) -> SolanaDTO:
        return SolanaDTO(**solana_dict)

    @staticmethod
    def dto_to_sqlalchemy(dto: SolanaDTO) -> SolanaSQLAlchemy:
        # Преобразуем DTO в модель SQLAlchemy
        return SolanaSQLAlchemy(
            price=dto.price,
            open=dto.open,
            close=dto.close,
            low=dto.low,
            high=dto.high,
            volume=dto.volume,
            time=dto.time,
        )

