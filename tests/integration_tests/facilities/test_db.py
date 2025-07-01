from src.schemas.facilities import FacilityAdd


async def test_add_facility(db):
    facility_data = FacilityAdd(title = "toilet")
    facility = await db.facilities.add(facility_data)
    await db.commit()
    assert facility
