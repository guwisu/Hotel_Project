from pydantic import BaseModel


class Hotel(BaseModel):
    title: str
    location: str


class HotelPATCH(BaseModel):
    title: str | None = None
    location: str | None = None
