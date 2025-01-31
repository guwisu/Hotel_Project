from fastapi import Query, Body, APIRouter

from dependencies import PaginationDep
from schemas.hotels import Hotel, HotelPATCH

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
def get_hotels(
        pagination: PaginationDep,
        id: int | None = Query(None, description="Айдишник:"),
        title: str | None = Query(None, description="Название отеля:"),
):
    hotels_ = []
    for hotel in hotels:
        if id and hotel["id"] != id:
            continue
        if title and hotel["title"] != title:
            continue
        hotels_.append(hotel)

    if pagination.page and pagination.per_page:
        return hotels_[pagination.per_page * (pagination.page - 1):][:pagination.per_page]
    return hotels_


@router.post("", summary="Добавить отель",)
def create_hotel(hotel_data: Hotel = Body(openapi_examples={
    "1": {"summary": "Сочи", "value": {
        "title": "Отель Сочи 5 звезд у моря",
        "name": "sochi_u_morya",
    }},
    "2": {"summary": "Дубай", "value": {
        "title": "Отель Дубай у фонтана",
        "name": "dubai_fountain",
    }},
})
):
    global hotels
    hotels.append({
        "id": hotels[-1]["id"] + 1,
        "title": hotel_data.title,
        "name": hotel_data.name,
    })
    return {"status": "OK"}


@router.delete("/{hotel_id}", summary="Удалить отель",)
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": "OK"}


@router.patch("/{hotel_id}",
           summary="Частично изменить данные об отеле",
           description="<h1>Тут мы можем частично поменять данные об отеле: отправит либо name, либо title</h1>"
           )
def patch_hotel(
        hotel_id: int,
        hotel_data: HotelPATCH,
):
    global hotels
    if hotel_data.title:
        hotels[hotel_id - 1]["title"] = hotel_data.title
    if hotel_data.name:
        hotels[hotel_id - 1]["name"] = hotel_data.name
    return {"status": "OK"}


@router.put("/{hotel_id}", summary="Изменить данные об отеле")
def put_hotel(hotel_id: int, hotel_data: Hotel,):
    global hotels
    hotels[hotel_id - 1]["title"] = hotel_data.title
    hotels[hotel_id - 1]["name"] = hotel_data.name
    return {"status": "OK"}
