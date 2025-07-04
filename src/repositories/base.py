from typing import Sequence


from sqlalchemy import select, insert, update, delete
from sqlalchemy.exc import NoResultFound, IntegrityError
from pydantic import BaseModel

from src.exceptions import ObjectNotFoundException, UserAlreadyExistsException
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

    async def get_all(
        self,
    ):
        return await self.get_filtered()

    async def get_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        model = result.scalars().one_or_none()
        if model is None:
            return None
        return self.mapper.map_to_domain_entity(model)

    async def get_one(self, **filter_by) -> BaseModel:
        "asyncpg.exceptions.DataError"
        "sqlalchemy.dialects.postgresql.asyncpg.Error"
        "sqlalchemy.exc.DBAPIError"
        "sqlalchemy.exc.NoResultFound"
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
        except IntegrityError:
            raise ObjectNotFoundException
        return self.mapper.map_to_domain_entity(model)

    async def add_user(self, data: BaseModel):
        try:
            add_data_stmt = insert(self.model).values(**data.model_dump()).returning(self.model)
            result = await self.session.execute(add_data_stmt)
            model = result.scalars().one()
        except IntegrityError:
            raise UserAlreadyExistsException
        return self.mapper.map_to_domain_entity(model)

    async def add_bulk(self, data: Sequence[BaseModel]):
        add_data_stmt = insert(self.model).values([item.model_dump() for item in data])
        await self.session.execute(add_data_stmt)

    async def edit(self, data: BaseModel, exclude_unset: bool = False, **filter_by) -> None:
        try:
            update_stmt = (
                update(self.model)
                .filter_by(**filter_by)
                .values(**data.model_dump(exclude_unset=exclude_unset))
            )
        except NoResultFound:
            raise ObjectNotFoundException
        await self.session.execute(update_stmt)

    async def edit_bulk(self, data: list[int], **filter_by) -> None:
        update_stmt = update(self.model).filter_by(**filter_by).values([item for item in data])
        await self.session.execute(update_stmt)

    async def delete(self, **filter_by) -> None:
        try:
            delete_stmt = delete(self.model).filter_by(**filter_by)
        except NoResultFound:
            raise ObjectNotFoundException
        await self.session.execute(delete_stmt)
