from src.schemas.hotels import HotelAdd



async def test_add_hotel(db):
    hotel_data = HotelAdd(title="Best hotel eveeer", location="Сочи")
    await db.hotels.add(hotel_data)
    await db.commit()

async def test_add_hotel2(db):
    hotel_data = HotelAdd(title="VIP 5 stars +", location="Дубай")
    await db.hotels.add(hotel_data)
    await db.commit()

