from datetime import date

from platformdirs import user_state_dir

from src.repositories.utils import rooms_ids_for_booking
from src.schemas.bookings import BookingAdd
from src.schemas.hotels import HotelAdd

#CRUD CREATE READ UPDATE DELETE
async def test_booking_crud(db):
    user_id = (await db.users.get_all())[0].id
    room_id = (await db.rooms.get_all())[0].id
    booking_data = BookingAdd(
        user_id = user_id,
        room_id = room_id,
        date_from=date(year=2025, month=6, day=30),
        date_to=date(year=2025, month=7, day=1),
        price = 1337,
    )
    await db.bookings.add(booking_data)

    assert db.bookings.get_one_or_none(user_id=user_id, room_id=room_id)

    new_booking_data = BookingAdd(
        user_id=user_id,
        room_id=room_id,
        date_from=date(year=2025, month=7, day= 1),
        date_to=date(year=2025, month=7, day= 31),
        price=525,
    )

    await db.bookings.edit(new_booking_data)

    #await db.bookings.delete(user_id=user_id, room_id=room_id)

    await db.commit()