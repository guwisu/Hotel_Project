from fastapi import Query, Body, APIRouter

from src.api.dependencies import PaginationDep, DBDep
from src.schemas.hotels import HotelPatch, HotelAdd

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("", summary="Получить список отелей",)
async def get_hotels(
        pagination: PaginationDep,
        db: DBDep,
        location: str | None = Query(None, description="Адрес отеля:"),
        title: str | None = Query(None, description="Название отеля:"),
):
    per_page = pagination.per_page or 5
    return await db.hotels.get_all(
        location=location,
        title=title,
        limit=per_page,
        offset=per_page * (pagination.page - 1)
    )


@router.get("/{hotel_id}", summary="Получение отеля по айдишнику")
async def get_hotel(hotel_id: int, db: DBDep):
    return await db.hotels.get_one_or_none(id=hotel_id)


@router.post("", summary="Добавить отель",)
async def create_hotel(db: DBDep, hotel_data: HotelAdd = Body(openapi_examples={
    "1": {"summary": "Сочи", "value": {
        "title": "Отель VIP 5 звезд у моря",
        "location": "Сочи ул. Моря, 1",
    }},
    "2": {"summary": "Дубай", "value": {
        "title": "Отель Lux у фонтана",
        "location": "Дубай ул. Шейха, 2",
    }},
})
):
    hotel = await db.hotels.add(hotel_data)
    await db.commit()

    return {"status": "OK", "data": hotel}


@router.delete("/{hotel_id}", summary="Удалить отель",)
async def delete_hotel(db: DBDep, hotel_id: int):
    await db.hotels.delete(id=hotel_id)
    await db.commit()
    return {"status": "OK"}


@router.patch("/{hotel_id}",
           summary="Частично изменить данные об отеле",
           description="<h1>Тут мы можем частично поменять данные об отеле: отправит либо name, либо title</h1>"
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





