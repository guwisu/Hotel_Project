from src.exceptions import FacilityAlreadyExistsException, FacilityEmptyDataException
from src.schemas.facilities import FacilityAdd
from src.services.base import BaseService
from src.tasks.tasks import test_task


class FacilityService(BaseService):
    async def get_facilities(self):
        return await self.db.facilities.get_all()

    async def add_facility(self, facility_data: FacilityAdd):
        facilities = await self.db.facilities.get_all()
        facilities_title = [item.title for item in facilities]
        if facility_data.title in facilities_title:
            raise FacilityAlreadyExistsException
        if not facility_data.title:
            raise FacilityEmptyDataException
        facility = await self.db.facilities.add(data=facility_data)
        await self.db.commit()

        test_task.delay()

        return facility
