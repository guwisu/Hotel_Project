from datetime import date

from src.exceptions import check_date_to_after_date_from, HotelNotFoundException, ObjectNotFoundException, \
    RoomNotFoundException, FacilityNotFoundException, RoomEmptyDataException, HotelAndRoomNotRelatedException
from src.schemas.facilities import RoomFacilityAdd
from src.schemas.rooms import RoomAdd, Room, RoomAddRequest, RoomPatchRequest, RoomPatch
from src.services.base import BaseService
from src.services.hotels import HotelService


class RoomService(BaseService):
    async def get_filtered_by_time(
        self,
        hotel_id: int,
        date_from: date,
        date_to: date
    ):
        check_date_to_after_date_from(date_from, date_to)
        try:
            await HotelService(self.db).get_hotel_with_check(hotel_id)
        except ObjectNotFoundException:
            raise HotelNotFoundException
        return await self.db.rooms.get_filtered_by_time(
            hotel_id=hotel_id, date_from=date_from, date_to=date_to
        )

    async def get_room(
            self,
            hotel_id: int,
            room_id: int,
    ):
        return await self.db.rooms.get_one_with_rels(id=room_id, hotel_id=hotel_id)

    async def create_room(
            self,
            hotel_id: int,
            room_data: RoomAddRequest
    ):
        if not room_data.title or not room_data.description:
            raise RoomEmptyDataException
        try:
            await self.db.hotels.get_one(id=hotel_id)
        except ObjectNotFoundException as ex:
            raise HotelNotFoundException from ex
        _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
        room = await self.db.rooms.add(_room_data)

        rooms_facilities_data = [
            RoomFacilityAdd(room_id=room.id, facility_id=f_id) for f_id in room_data.facilities_ids
        ]
        if room_data.facilities_ids:
            try:
                await self.db.rooms_facilities.add_bulk(rooms_facilities_data)
            except ObjectNotFoundException:
                raise FacilityNotFoundException
        await self.db.commit()
        return room

    async def partially_edit_room(
            self,
            hotel_id: int,
            room_id: int,
            room_data: RoomPatchRequest
    ):
        if not room_data.title and not room_data.description:
            raise RoomEmptyDataException
        hotel = await HotelService(self.db).get_hotel_with_check(hotel_id)
        room = await self.get_room_with_check(room_id)
        if room.hotel_id != hotel.id:
            raise HotelAndRoomNotRelatedException

        _room_data_dict = room_data.model_dump(exclude_unset=True)

        _room_data = RoomPatch(hotel_id=hotel_id, **_room_data_dict)

        room = await self.db.rooms.edit(_room_data, exclude_unset=True, id=room_id, hotel_id=hotel_id)
        try:
            if "facilities_ids" in _room_data_dict:
                await self.db.rooms_facilities.set_room_facilities(
                    room_id, facilities_ids=_room_data_dict["facilities_ids"]
                )
        except ObjectNotFoundException:
            raise FacilityNotFoundException
        await self.db.commit()
        return room

    async def edit_room(
            self,
            hotel_id: int,
            room_id: int,
            room_data: RoomAddRequest
    ):
        if not room_data.title or not room_data.description:
            raise RoomEmptyDataException
        hotel = await HotelService(self.db).get_hotel_with_check(hotel_id)
        room = await self.get_room_with_check(room_id)
        if room.hotel_id != hotel.id:
            raise HotelAndRoomNotRelatedException
        _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
        room = await self.db.rooms.edit(_room_data, id=room_id)
        try:
            await self.db.rooms_facilities.set_room_facilities(room_id, facilities_ids=room_data.facilities_ids)
        except ObjectNotFoundException:
            raise FacilityNotFoundException
        await self.db.commit()
        return room

    async def delete_room(
            self,
            hotel_id: int,
            room_id: int
    ):

        hotel = await HotelService(self.db).get_hotel_with_check(hotel_id)
        room = await self.get_room_with_check(room_id)
        if room.hotel_id != hotel.id:
            raise HotelAndRoomNotRelatedException
        await self.db.rooms_facilities.set_room_facilities(room_id, [])
        try:
            await self.db.rooms.delete(id=room_id, hotel_id=hotel_id)
            await self.db.commit()
        except ObjectNotFoundException:
            raise RoomNotFoundException

    async def get_room_with_check(self, room_id: int) -> Room:
        try:
            return await self.db.rooms.get_one(id=room_id)
        except ObjectNotFoundException:
            raise RoomNotFoundException