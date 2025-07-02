import pytest
from unittest import mock

from wheel.metadata import yield_lines

mock.patch("fastapi_cache.decorator.cache",  lambda *args, **kwargs: lambda f: f).start()

from json import load
from httpx import AsyncClient

from src.api.dependencies import get_db
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

async def get_db_null_pool():
    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        yield db

@pytest.fixture(scope="function")
async def db():
    async for db in get_db_null_pool():
        yield db

app.dependency_overrides[get_db] = get_db_null_pool


@pytest.fixture(scope="session", autouse=True)
async def setup_database(check_test_mod):
    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    with open("tests/mock_hotels.json", encoding="utf-8") as file_hotels:
        hotels = [HotelAdd.model_validate(hotel) for hotel in load(file_hotels)]

    with open("tests/mock_rooms.json", encoding="utf-8") as file_rooms:
        rooms = [RoomAdd.model_validate(room) for room in load(file_rooms)]

    async with DBManager(session_factory=async_session_maker_null_pool) as db_:
        await db_.hotels.add_bulk(hotels)
        await db_.rooms.add_bulk(rooms)
        await db_.commit()

@pytest.fixture(scope="session")
async def ac():
    async with AsyncClient(app=app, base_url="https://test") as ac:
        yield ac


@pytest.fixture(scope="session", autouse=True)
async def register_user(ac, setup_database):
    await ac.post(
        "/auth/register",
        json={
            "email": "cat@dog.com",
            "password": "1234",
            }
        )

@pytest.fixture(scope="session", autouse=True)
async def authenticated_ac(ac, register_user):
    response = await ac.post(
        "/auth/login",
        json={
            "email": "cat@dog.com",
            "password": "1234",
        }
    )
    token = response.cookies.get("access_token")
    assert token
    yield ac
