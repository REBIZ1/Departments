import logging

from asyncpg import UniqueViolationError
from pydantic import BaseModel
from sqlalchemy import insert, update, delete, select
from sqlalchemy.exc import NoResultFound, IntegrityError

from src.exceptions.exceptions import (
    ObjectAlreadyExistsException,
    ObjectNotFoundException,
)
from src.repositories.mappers.base import DataMapper


class BaseRepository:
    model = None
    mapper: DataMapper

    def __init__(self, session):
        self.session = session

    async def get_filtered(self, *filter, **filter_by):
        """
        Возвращает отфильтрованные данные
        """
        query = select(self.model).filter(*filter).filter_by(**filter_by)
        result = await self.session.execute(query)
        return [self.mapper.map_to_domain_entity(obj) for obj in result.scalars().all()]

    async def get_one(self, *filter, **filter_by):
        """
        Принимает аргументы для фильтрации и возвращает одно значение
        """
        query = select(self.model).filter(*filter).filter_by(**filter_by)
        result = await self.session.execute(query)
        try:
            obj = result.scalars().one()
        except NoResultFound:
            raise ObjectNotFoundException
        return self.mapper.map_to_domain_entity(obj)

    async def add(self, data: BaseModel):
        """
        Добавляет данные в бд
        """
        try:
            add_stmt = (
                insert(self.model).values(**data.model_dump()).returning(self.model)
            )
            result = await self.session.execute(add_stmt)
            obj = result.scalars().one()
            return self.mapper.map_to_domain_entity(obj)
        except IntegrityError as e:
            logging.error(
                f"Не удалось добавить данные в БД, тип ошибки: {type(e.orig.__cause__)=}"
            )
            if isinstance(e.orig.__cause__, UniqueViolationError):
                raise ObjectAlreadyExistsException from e
            else:
                logging.error(
                    f"Незнакомая ошибка, тип ошибки: {type(e.orig.__cause__)=}"
                )
                raise e

    async def edit(self, data: BaseModel, exclude_unset: bool = False, **filter_by):
        """
        Изменяет данные в БД, если exclude_unset = True, то изменяет частично
        """
        edit_stmt = (
            update(self.model)
            .filter_by(**filter_by)
            .values(**data.model_dump(exclude_unset=exclude_unset))
            .returning(self.model)
        )
        result = await self.session.execute(edit_stmt)
        obj = result.scalars().one()
        return self.mapper.map_to_domain_entity(obj)

    async def delete(self, **filter_by):
        """
        Удаляет данные из БД
        """
        delete_stmt = delete(self.model).filter_by(**filter_by)
        await self.session.execute(delete_stmt)

    async def reassign(self, old_id: int, new_id: int | None, field_name: str):
        """
        Массово обновляет значение внешнего ключа у записей модели
        """
        field = getattr(self.model, field_name)
        stmt = update(self.model).where(field == old_id).values({field_name: new_id})
        await self.session.execute(stmt)
