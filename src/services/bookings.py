from src.api.dependencies import UserIdDep
from src.exceptions import AllRoomsAreBookedException, check_date_to_after_date_from, UserNotAuthenticatedException
from src.schemas.bookings import BookingAddRequest, BookingAdd
from src.services.base import BaseService
from src.services.hotels import HotelService
from src.services.rooms import RoomService


class BookingService(BaseService):
    async def get_bookings(self):
        return await self.db.bookings.get_all()

    async def get_my_bookings(self, user_id: int):
        return await self.db.bookings.get_filtered(user_id=user_id)

    async def add_booking(
            self,
            user_id: UserIdDep,
            booking_data: BookingAddRequest,
    ):
        if not user_id:
            raise UserNotAuthenticatedException
        check_date_to_after_date_from(booking_data.date_from, booking_data.date_to)
        room = await RoomService(self.db).get_room_with_check(booking_data.room_id)
        hotel = await HotelService(self.db).get_hotel_with_check(room.hotel_id)
        room_price: int = room.price
        _booking_data = BookingAdd(
            user_id=user_id,
            price=room_price,
            **booking_data.dict(),
        )
        try:
            booking = await self.db.bookings.add_booking(_booking_data, hotel_id=hotel.id)
        except AllRoomsAreBookedException as ex:
            raise ex
        await self.db.commit()
        return booking