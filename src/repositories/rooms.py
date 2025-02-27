from src.models.rooms import RoomsOrm
from src.repositories.base import BaseRepository
from src.schemas.rooms import Room
from sqlalchemy import select, func


class RoomsRepository(BaseRepository):
    model = RoomsOrm
    schema = Room

    async def get_all(
            self,
            title,
            description,
            price,
            quantity,
    ) -> list[Room]:
        query = select(RoomsOrm)
        if title:
            query = query.filter(func.lower(RoomsOrm.title).contains(title.strip().lower()))
        if description:
            query = query.filter(func.lower(RoomsOrm.description).contains(description.strip().lower()))
        if price is not None:
            query = query.where(RoomsOrm.price == price)
        if quantity is not None:
            query = query.where(RoomsOrm.quantity == quantity)

        print(query.compile(compile_kwargs={"literal_binds": True}))
        result = await self.session.execute(query)
        return [Room.model_validate(hotel, from_attributes=True) for hotel in result.scalars().all()]
