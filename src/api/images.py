from fastapi import APIRouter, UploadFile, BackgroundTasks

from src.services.images import ImageService


router = APIRouter(prefix="/images", tags=["Изображения отелей"])


@router.post("")
def upload_image(file: UploadFile, background_tasks: BackgroundTasks):
    ImageService().upload_image(file, background_tasks)