import pytest

from src.database import async_session_maker_null_pool
from src.utils.db_manager import DBManager


@pytest.mark.parametrize("room_id, date_from, date_to, status_code", [
    (1, "2025-07-01", "2025-07-10", 200),
    (1, "2025-07-02", "2025-07-11", 200),
    (1, "2025-07-03", "2025-07-12", 200),
    (1, "2025-07-04", "2025-07-13", 200),
    (1, "2025-07-05", "2025-07-14", 200),
    (1, "2025-07-06", "2025-07-15", 404),
    (1, "2025-07-26", "2025-07-30", 200),
])
async def test_add_booking(
    room_id, date_from, date_to, status_code,
    authenticated_ac
):
    response = await authenticated_ac.post(
        "/bookings",
        json={
            "room_id": room_id,
            "date_from": date_from,
            "date_to": date_to,
        }
    )
    assert response.status_code == status_code
    if status_code == 200:
        res = response.json()
        assert isinstance(res, dict)
        assert res["status"] == "OK"
        assert "data" in res

@pytest.fixture(scope="module")
async def delete_all_bookings():
    async with DBManager(session_factory=async_session_maker_null_pool) as db_:
        await db_.bookings.delete()
        await db_.commit()

@pytest.mark.parametrize("room_id, date_from, date_to, status_code, quantity", [
    (1, "2025-07-01", "2025-07-10", 200, 1),
    (1, "2025-07-02", "2025-07-11", 200, 2),
    (1, "2025-07-03", "2025-07-12", 200, 3),
])
async def test_add_and_get_bookings(
    room_id, date_from, date_to, status_code, quantity,
    authenticated_ac,
    delete_all_bookings,
):
    response = await authenticated_ac.post(
        "/bookings",
        json = {
            "room_id": room_id,
            "date_from": date_from,
            "date_to": date_to,
        }
    )
    response_quantity = await authenticated_ac.get(
        "/bookings/me"
    )
    assert len(response_quantity.json()) == quantity
    assert response.status_code == status_code
    if status_code == 200:
        res = response.json()
        assert isinstance(res, dict)
        assert res["status"] == "OK"
        assert "data" in res
