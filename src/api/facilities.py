from fastapi import APIRouter, Body
from fastapi_cache.decorator import cache

from src.api.dependencies import DBDep
from src.exceptions import (
    FacilityAlreadyExistsException,
    FacilityAlreadyExistsHTTPException,
    FacilityEmptyDataException,
    FacilityEmptyDataHTTPException,
)
from src.schemas.facilities import FacilityAdd
from src.services.facilities import FacilityService

router = APIRouter(prefix="/facilities", tags=["Удобства"])


@router.get("")
@cache(expire=10)
async def get_facilities(db: DBDep):
    return await FacilityService(db).get_facilities()


@router.post("")
async def add_facility(
    db: DBDep,
    facility_data: FacilityAdd = Body(),
):
    try:
        facility = await FacilityService(db).add_facility(facility_data)
        return {"status": "OK", "data": facility}
    except FacilityAlreadyExistsException:
        raise FacilityAlreadyExistsHTTPException
    except FacilityEmptyDataException:
        raise FacilityEmptyDataHTTPException
