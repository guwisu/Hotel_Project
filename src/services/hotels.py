from datetime import date

from sqlalchemy.exc import NoResultFound

from src.exceptions import check_date_to_after_date_from, HotelNotFoundException, ObjectNotFoundException, \
    HotelAlreadyExistsException, HotelEmptyDataException
from src.schemas.hotels import HotelAdd, HotelPatch, Hotel
from src.services.base import BaseService


class HotelService(BaseService):
    async def get_filtered_by_time(
        self,
        pagination,
        location: str | None,
        title: str | None,
        date_from: date ,
        date_to: date ,
    ):
        check_date_to_after_date_from(date_from, date_to)
        per_page = pagination.per_page or 5
        return await self.db.hotels.get_filtered_by_time(
            date_from=date_from,
            date_to=date_to,
            location=location,
            title=title,
            limit=per_page,
            offset=per_page * (pagination.page - 1),
        )

    async def get_hotel(self, hotel_id: int):
        return await self.db.hotels.get_one(id=hotel_id)

    async def get_hotels(self):
        return await self.db.hotels.get_all()

    async def add_hotel(self, hotel_data: HotelAdd):
        all_hotels = await self.get_hotels()
        if not hotel_data.title or not hotel_data.location:
            raise HotelEmptyDataException
        if [hotel.title for hotel in all_hotels if hotel.title == hotel_data.title]:
            raise HotelAlreadyExistsException

        hotel = await self.db.hotels.add(hotel_data)
        await self.db.commit()
        return hotel

    async def delete_hotel(self, hotel_id: int):
        await self.get_hotel_with_check(hotel_id=hotel_id)
        await self.db.rooms.delete(hotel_id=hotel_id)
        await self.db.hotels.delete(id=hotel_id)
        await self.db.commit()



    async def edit_hotel_partially(self, hotel_id: int, hotel_data: HotelPatch, exclude_unset: bool):
        if not hotel_data.title and not hotel_data.location:
            raise HotelEmptyDataException
        try:
            hotel = await self.db.hotels.edit(hotel_data, exclude_unset, id=hotel_id)
            await self.db.commit()
            return hotel
        except NoResultFound:
            raise HotelNotFoundException


    async def edit_hotel(self, hotel_id: int, hotel_data: HotelPatch):
        if not hotel_data.title or not hotel_data.location:
            raise HotelEmptyDataException
        try:
            hotel = await self.db.hotels.edit(hotel_data, id=hotel_id)
            await self.db.commit()
            return hotel
        except NoResultFound:
            raise HotelNotFoundException

    async def get_hotel_with_check(self, hotel_id: int) -> Hotel:
        try:
            return await self.db.hotels.get_one(id=hotel_id)
        except ObjectNotFoundException:
            raise HotelNotFoundException

