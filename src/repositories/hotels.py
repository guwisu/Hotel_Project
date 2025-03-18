from datetime import date

from sqlalchemy import select, func

from src.models.rooms import RoomsOrm
from src.repositories.base import BaseRepository
from src.models.hotels import HotelsOrm
from src.repositories.utils import rooms_ids_for_booking
from src.schemas.hotels import Hotel


class HotelsRepository(BaseRepository):
    model = HotelsOrm
    schema = Hotel

    # async def get_all(
    #         self,
    #         location,
    #         title,
    #         limit,
    #         offset,
    # ) -> list[Hotel]:
    #     query = select(HotelsOrm)
    #     if location:
    #         query = query.filter(func.lower(HotelsOrm.location).contains(location.strip().lower()))
    #     if title:
    #         query = query.filter(func.lower(HotelsOrm.title).contains(title.strip().lower()))
    #     query = (
    #         query
    #         .limit(limit)
    #         .offset(offset)
    #     )
    #     print(query.compile(compile_kwargs={"literal_binds": True}))
    #     result = await self.session.execute(query)
    #     return [Hotel.model_validate(hotel, from_attributes=True) for hotel in result.scalars().all()]

    async def get_filtered_by_time(
            self,
            date_from: date,
            date_to: date,
            location,
            title,
            limit,
            offset,
    ):
        rooms_ids_to_get = rooms_ids_for_booking(date_from=date_from, date_to=date_to)
        hotels_ids_to_get = (
            select(RoomsOrm.hotel_id)
            .select_from(RoomsOrm)
            .filter(RoomsOrm.id.in_(rooms_ids_to_get))
        )
        query = hotels_ids_to_get
        if location:
            query = query.filter(func.lower(HotelsOrm.location).contains(location.strip().lower()))
        if title:
            query = query.filter(func.lower(HotelsOrm.title).contains(title.strip().lower()))
        query = (
            query
            .limit(limit)
            .offset(offset)
        )
        # print(query.compile(compile_kwargs={"literal_binds": True}))
        # result = await self.session.execute(query)
        # return [Hotel.model_validate(hotel, from_attributes=True) for hotel in result.scalars().all()]

        return await self.get_filtered(HotelsOrm.id.in_(query))
