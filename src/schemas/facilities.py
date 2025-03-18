from pydantic import BaseModel, ConfigDict


class FacilityAddRequest(BaseModel):
    title: str


class FacilityAdd(BaseModel):
    title: str


class Facility(FacilityAdd):
    id: int

    model_config = ConfigDict(from_attributes=True)
