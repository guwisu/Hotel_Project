from json import load
import pytest
from httpx import AsyncClient

from src.config import settings
from src.database import Base, engine_null_pool, async_session_maker_null_pool
from src.main import app
from src.models import *
from src.schemas.hotels import HotelAdd
from src.schemas.rooms import RoomAdd
from src.utils.db_manager import DBManager


@pytest.fixture(scope="session", autouse=True)
def check_test_mod():
    assert settings.MODE == "TEST"


@pytest.fixture(scope="session", autouse=True)
async def setup_database(check_test_mod):
    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    with open("tests/mock_hotels.json", encoding="utf-8") as hotels:
        hotels = [HotelAdd.model_validate(hotel) for hotel in load(hotels)]

    with open("tests/mock_rooms.json", encoding="utf-8") as rooms:
        rooms = [RoomAdd.model_validate(room) for room in load(rooms)]

    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        await db.hotels.add_bulk(hotels)
        await db.rooms.add_bulk(rooms)
        await db.commit()

@pytest.fixture(scope="session", autouse=True)
async def register_user(setup_database):
    async with AsyncClient(app=app, base_url="https://test") as ac:
        await ac.post(
            "/auth/register",
            json={
                "email": "cat@dog.com",
                  "password": "1234",
                }
            )