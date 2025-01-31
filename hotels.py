from fastapi import Query, Body, APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/hotels")

hotels = [
    {"id": 1, "title": "Sochi", "name": "sochi"},
    {"id": 2, "title": "Dubai", "name": "dubai"},
]


@router.get("",
         summary="Получить список отелей",
         )
def get_hotels(
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
    return hotels_


class Hotel(BaseModel):
    title: str = Body(),
    name: str = Body(),


@router.post("",
          summary="Добавить отель",
          )
def create_hotel(hotel_data: Hotel):
    global hotels
    hotels.append({
        "id": hotels[-1]["id"] + 1,
        "title": hotel_data.title,
        "name": hotel_data.name,
    })
    return {"status": "OK"}


@router.put("/{hotel_id}",
         summary="Изменить данные об отеле",
         )
def put_hotel(hotel_id: int, hotel_data: Hotel,):
    global hotels
    hotels[hotel_id - 1]["title"] = hotel_data.title
    hotels[hotel_id - 1]["name"] = hotel_data.name
    return {"status": "OK"}


@router.patch("/{hotel_id}",
           summary="Частично изменить данные об отеле",
           description="<h1>Тут мы можем частично поменять данные об отеле: отправит либо name, либо title</h1>"
           )
def patch_hotel(
        hotel_id: int,
        title: str | None = Body(None),
        name: str | None = Body(None),
):
    global hotels
    if title:
        hotels[hotel_id - 1]["title"] = title
    if name:
        hotels[hotel_id - 1]["name"] = name
    return {"status": "OK"}


@router.delete("/{hotel_id}",
            summary="Удалить отель",
            )
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": "OK"}
