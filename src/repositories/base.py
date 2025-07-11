import logging
from typing import Sequence

from asyncpg.exceptions import UniqueViolationError
from sqlalchemy import select, insert, update, delete
from sqlalchemy.exc import NoResultFound, IntegrityError
from pydantic import BaseModel

from src.exceptions import ObjectNotFoundException, ObjectAlreadyExistsException
from src.repositories.mappers.base import DataMapper


class BaseRepository:
    model = None
    mapper: DataMapper = None

    def __init__(self, session):
        self.session = session

    async def get_filtered(self, *filter, **filter_by):
        query = select(self.model).filter(*filter).filter_by(**filter_by)
        result = await self.session.execute(query)
        return [self.mapper.map_to_domain_entity(model) for model in result.scalars().all()]

    async def get_all(self):
        return await self.get_filtered()

    async def get_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        model = result.scalars().one_or_none()
        if model is None:
            return None
        return self.mapper.map_to_domain_entity(model)

    async def get_one(self, **filter_by) -> BaseModel:
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        try:
            model = result.scalars().one()
        except NoResultFound:
            raise ObjectNotFoundException
        return self.mapper.map_to_domain_entity(model)

    async def add(self, data: BaseModel):
        try:
            add_data_stmt = insert(self.model).values(**data.model_dump()).returning(self.model)
            result = await self.session.execute(add_data_stmt)
            model = result.scalars().one()
            return self.mapper.map_to_domain_entity(model)
        except IntegrityError as ex:
            logging.exception(
                f"Не удалось добавить данные в БД, входные данные={data}"
            )
            if isinstance(ex.orig.__cause__, UniqueViolationError):
                raise ObjectAlreadyExistsException from ex
            else:
                logging.exception(
                    f"Незнакомая ошибка: не удалось добавить данные в БД, входные данные={data}"
                )
                raise ex

    async def add_bulk(self, data: Sequence[BaseModel]):
        try:
            add_data_stmt = insert(self.model).values([item.model_dump() for item in data])
            await self.session.execute(add_data_stmt)
        except IntegrityError:
            raise ObjectNotFoundException
    async def edit(self, data: BaseModel, exclude_unset: bool = False, **filter_by):
        try:
            update_stmt = (
                update(self.model)
                .filter_by(**filter_by)
                .values(**data.model_dump(exclude_unset=exclude_unset))
                .returning(self.model)
            )
        except NoResultFound:
            raise ObjectNotFoundException
        result = await self.session.execute(update_stmt)
        model = result.scalars().one()
        return self.mapper.map_to_domain_entity(model)


    async def edit_bulk(self, data: list[int], **filter_by) -> None:
        update_stmt = update(self.model).filter_by(**filter_by).values([item for item in data])
        await self.session.execute(update_stmt)

    async def delete(self, **filter_by) -> None:
        try:
            delete_stmt = delete(self.model).filter_by(**filter_by)
        except NoResultFound:
            raise ObjectNotFoundException
        await self.session.execute(delete_stmt)
