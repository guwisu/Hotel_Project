from fastapi import Query, Body, APIRouter

from sqlalchemy import insert, select

from src.api.dependencies import PaginationDep
from src.database import async_session_maker, engine
from src.models.hotels import HotelsOrm
from src.repositories.hotels import HotelsRepository
from src.schemas.hotels import Hotel, HotelPATCH

router = APIRouter(prefix="/hotels")

hotels = [
    {"id": 1, "title": "Sochi", "name": "sochi"},
    {"id": 2, "title": "Дубай", "name": "dubai"},
    {"id": 3, "title": "Мальдивы", "name": "maldivi"},
    {"id": 4, "title": "Геленджик", "name": "gelendzhik"},
    {"id": 5, "title": "Москва", "name": "moscow"},
    {"id": 6, "title": "Казань", "name": "kazan"},
    {"id": 7, "title": "Санкт-Петербург", "name": "spb"},
]


@router.get("", summary="Получить список отелей",)
async def get_hotels(
        pagination: PaginationDep,
        location: str | None = Query(None, description="Адрес отеля:"),
        title: str | None = Query(None, description="Название отеля:"),
):
    per_page = pagination.per_page or 5
    async with async_session_maker() as session:
        return await HotelsRepository(session).get_all(
            location=location,
            title=title,
            limit=per_page,
            offset=per_page * (pagination.page - 1)
        )


@router.post("", summary="Добавить отель",)
async def create_hotel(hotel_data: Hotel = Body(openapi_examples={
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
    async with async_session_maker() as session:
        hotel = await HotelsRepository(session).add(hotel_data)
        await session.commit()
    return {"status": "OK", "data": hotel}


@router.delete("/{hotel_id}", summary="Удалить отель",)
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": "OK"}


@router.patch("/{hotel_id}",
           summary="Частично изменить данные об отеле",
           description="<h1>Тут мы можем частично поменять данные об отеле: отправит либо name, либо title</h1>"
           )
def patch_hotel(hotel_id: int, hotel_data: HotelPATCH):
    global hotels
    hotel = [hotel for hotel in hotels if hotel["id"] == hotel_id][0]
    if hotel_data.title:
        hotel["title"] = hotel_data.title
    if hotel_data.name:
        hotel["name"] = hotel_data.name
    return {"status": "OK"}


@router.put("/{hotel_id}", summary="Изменить данные об отеле")
def put_hotel(hotel_id: int, hotel_data: Hotel):
    global hotels
    hotel = [hotel for hotel in hotels if hotel["id"] == hotel_id][0]
    hotel["title"] = hotel_data.title
    hotel["name"] = hotel_data.name
    return {"status": "OK"}





