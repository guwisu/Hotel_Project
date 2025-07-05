from datetime import date

from fastapi import Query, Body, APIRouter, HTTPException
from fastapi_cache.decorator import cache

from src.api.dependencies import PaginationDep, DBDep
from src.exceptions import IncorrectDateException, ObjectNotFoundException
from src.schemas.hotels import HotelPatch, HotelAdd

router = APIRouter(prefix="/hotels", tags=["Отели"])


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
    date_from: date = Query(example="2025-03-07"),
    date_to: date = Query(example="2025-03-15"),
):
    per_page = pagination.per_page or 5
    try:
        return await db.hotels.get_filtered_by_time(
            date_from=date_from,
            date_to=date_to,
            location=location,
            title=title,
            limit=per_page,
            offset=per_page * (pagination.page - 1),
        )
    except IncorrectDateException as ex:
        raise HTTPException(status_code=400, detail=ex.detail)


@router.get("/{hotel_id}", summary="Получение отеля по айдишнику")
async def get_hotel(hotel_id: int, db: DBDep):
    try:
        return await db.hotels.get_one(id=hotel_id)
    except ObjectNotFoundException:
        raise HTTPException(status_code=404, detail="Отель с таким id не найден")


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
    hotel = await db.hotels.add(hotel_data)
    await db.commit()

    return {"status": "OK", "data": hotel}


@router.delete(
    "/{hotel_id}",
    summary="Удалить отель",
)
async def delete_hotel(db: DBDep, hotel_id: int):
    await db.hotels.delete(id=hotel_id)
    await db.commit()
    return {"status": "OK"}


@router.patch(
    "/{hotel_id}",
    summary="Частично изменить данные об отеле",
    description="<h1>Тут мы можем частично поменять данные об отеле: отправит либо name, либо title</h1>",
)
async def patch_hotel(db: DBDep, hotel_id: int, hotel_data: HotelPatch):
    await db.hotels.edit(hotel_data, exclude_unset=True, id=hotel_id)
    await db.commit()
    return {"status": "OK"}


@router.put("/{hotel_id}", summary="Изменить данные об отеле")
async def edit_hotel(db: DBDep, hotel_id: int, hotel_data: HotelAdd):
    await db.hotels.edit(hotel_data, id=hotel_id)
    await db.commit()
    return {"status": "OK"}
