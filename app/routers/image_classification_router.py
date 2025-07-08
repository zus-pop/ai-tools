from fastapi import APIRouter, UploadFile
from ..ai_models import ImageClassifier
from ..dtos import IsNSFW

deepface_model = ImageClassifier()

router = APIRouter(
    prefix="/image-classification",
    tags=["Image Classification"],
)

@router.post("/")
def get_face_verification(selfie_image: UploadFile, profile_images: list[UploadFile]):
    return deepface_model.verify(selfie_image=selfie_image, profile_images=profile_images)

@router.post("/nsfw-detection")
def is_nsfw(image: UploadFile) -> IsNSFW:
    return deepface_model.is_nsfw(image=image.file.read())
