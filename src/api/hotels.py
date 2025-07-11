from datetime import date

from fastapi import Query, Body, APIRouter
from fastapi_cache.decorator import cache

from src.api.dependencies import PaginationDep, DBDep
from src.exceptions import (
    ObjectNotFoundException,
    HotelNotFoundHTTPException,
    HotelAlreadyExistsException,
    HotelAlreadyExistsHTTPException,
    HotelEmptyDataException,
    HotelEmptyDataHTTPException,
    HotelNotFoundException,
)
from src.schemas.hotels import HotelPatch, HotelAdd
from src.services.hotels import HotelService

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("/all", summary="Просто получить все отели")
async def get_all_hotels(db: DBDep):
    return await HotelService(db).get_hotels()


@router.get(
    "",
    summary="Получить список отелей",
)
@cache(expire=10)
async def get_hotels(
    pagination: PaginationDep,
    db: DBDep,
    location: str | None = Query(None, description="Адрес отеля:"),
    title: str | None = Query(None, description="Название отеля:"),
    date_from: date = Query(example="2025-07-07"),
    date_to: date = Query(example="2025-07-15"),
):
    return await HotelService(db).get_filtered_by_time(
        pagination,
        location,
        title,
        date_from,
        date_to,
    )


@router.get("/{hotel_id}", summary="Получение отеля по id")
async def get_hotel(hotel_id: int, db: DBDep):
    try:
        return await HotelService(db).get_hotel(hotel_id)
    except ObjectNotFoundException:
        raise HotelNotFoundHTTPException


@router.post(
    "",
    summary="Добавить отель",
)
async def create_hotel(
    db: DBDep,
    hotel_data: HotelAdd = Body(
        openapi_examples={
            "1": {
                "summary": "Сочи",
                "value": {
                    "title": "Отель VIP 5 звезд у моря",
                    "location": "Сочи ул. Моря, 1",
                },
            },
            "2": {
                "summary": "Дубай",
                "value": {
                    "title": "Отель Lux у фонтана",
                    "location": "Дубай ул. Шейха, 2",
                },
            },
        }
    ),
):
    try:
        hotel = await HotelService(db).add_hotel(hotel_data)
        return {"status": "OK", "data": hotel}
    except HotelEmptyDataException:
        raise HotelEmptyDataHTTPException
    except HotelAlreadyExistsException:
        raise HotelAlreadyExistsHTTPException


@router.delete(
    "/{hotel_id}",
    summary="Удалить отель",
)
async def delete_hotel(db: DBDep, hotel_id: int):
    try:
        await HotelService(db).delete_hotel(hotel_id)
        return {"status": "OK"}
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException


@router.patch(
    "/{hotel_id}",
    summary="Частично изменить данные об отеле",
    description="<h1>Тут мы можем частично поменять данные об отеле: отправит либо name, либо title</h1>",
)
async def patch_hotel(db: DBDep, hotel_id: int, hotel_data: HotelPatch):
    try:
        hotel = await HotelService(db).edit_hotel_partially(
            hotel_id, hotel_data, exclude_unset=True
        )
        return {"status": "OK", "data": hotel}
    except HotelEmptyDataException:
        raise HotelEmptyDataHTTPException
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException


@router.put("/{hotel_id}", summary="Изменить данные об отеле")
async def edit_hotel(db: DBDep, hotel_id: int, hotel_data: HotelPatch):
    try:
        hotel = await HotelService(db).edit_hotel(hotel_id, hotel_data)
        return {"status": "OK", "data": hotel}
    except HotelEmptyDataException:
        raise HotelEmptyDataHTTPException
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException
