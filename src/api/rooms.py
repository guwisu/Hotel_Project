from fastapi import Query, Body, APIRouter

from sqlalchemy import insert, select

from src.database import async_session_maker
from src.repositories.rooms import RoomsRepository
from src.schemas.rooms import Room, RoomAdd, RoomPATCH
from src.models.rooms import RoomsOrm

router = APIRouter(prefix="/hotels", tags=["Номера"])


@router.get("/{hotel_id}/rooms", summary="Получить список номеров")
async def get_rooms(
        # hotel_id: int,
        title: str = Query(None, description="Название номера"),
        description: str = Query(None, description="Описание Номера"),
        price: int = Query(None, description="Цена номера"),
        quantity: int = Query(None, description="Количество номеров"),
):
    async with async_session_maker() as session:
        return await RoomsRepository(session).get_all(
            title=title,
            description=description,
            price=price,
            quantity=quantity,
        )


@router.get("/{hotel_id}/{room_id}", summary="Получение номера по id")
async def get_room(
        room_id: int,
):
    async with async_session_maker() as session:
        return await RoomsRepository(session).get_one_or_none(id=room_id)


@router.post("/{hotel_id}", summary="Добавить номер")
async def create_room(room_data: RoomAdd):
    async with async_session_maker() as session:
        room = await RoomsRepository(session).add(room_data)
        await session.commit()

    return {"status": "OK", "data": room}


@router.delete("/{hotel_id}/{room_id}", summary="Удалить номер")
async def delete_room(room_id: int):
    async with async_session_maker() as session:
        await RoomsRepository(session).delete(id=room_id)
        await session.commit()
    return {"status": "OK"}


@router.patch("/{hotel_id}/{room_id}", summary="Частично изменить данные от номере")
async def patch_room(room_id: int, room_data: RoomPATCH):
    async with async_session_maker() as session:
        await RoomsRepository(session).edit(room_data, exclude_unset=True, id=room_id)
        await session.commit()
    return {"status": "OK"}


@router.put("/{hotel_id}/{room_id}", summary="Изменить данные об номере")
async def edit_room(room_id: int, room_data: RoomAdd):
    async with async_session_maker() as session:
        await RoomsRepository(session).edit(room_data, id=room_id)
        await session.commit()
    return {"status": "OK"}
