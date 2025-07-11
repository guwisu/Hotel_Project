import pytest

from tests.conftest import get_db_null_pool


@pytest.mark.parametrize(
    "room_id, date_from, date_to, status_code",
    [
        (1, "2025-07-01", "2025-07-10", 200),
        (1, "2025-07-02", "2025-07-11", 200),
        (1, "2025-07-03", "2025-07-12", 200),
        (1, "2025-07-04", "2025-07-13", 200),
        (1, "2025-07-05", "2025-07-14", 200),
        (1, "2025-07-06", "2025-07-15", 409),
        (1, "2025-07-26", "2025-07-30", 200),
    ],
)
async def test_add_booking(room_id, date_from, date_to, status_code, authenticated_ac):
    response = await authenticated_ac.post(
        "/bookings",
        json={
            "room_id": room_id,
            "date_from": date_from,
            "date_to": date_to,
        },
    )
    assert response.status_code == status_code
    if status_code == 200:
        res = response.json()
        assert isinstance(res, dict)
        assert res["status"] == "OK"
        assert "data" in res


@pytest.fixture(scope="module")
async def delete_all_bookings():
    async for _db in get_db_null_pool():
        await _db.bookings.delete()
        await _db.commit()


@pytest.mark.parametrize(
    "room_id, date_from, date_to, booked_qty",
    [
        (1, "2025-07-01", "2025-07-10", 1),
        (1, "2025-07-02", "2025-07-11", 2),
        (1, "2025-07-03", "2025-07-12", 3),
    ],
)
async def test_add_and_get_bookings(
    room_id,
    date_from,
    date_to,
    booked_qty,
    authenticated_ac,
    delete_all_bookings,
):
    response = await authenticated_ac.post(
        "/bookings",
        json={
            "room_id": room_id,
            "date_from": date_from,
            "date_to": date_to,
        },
    )
    assert response.status_code == 200
    response_quantity = await authenticated_ac.get("/bookings/me")
    assert response_quantity.status_code == 200
    assert len(response_quantity.json()) == booked_qty
