from fastapi import APIRouter, UploadFile
from ..ai_models import ImageClassifier

deepface_model = ImageClassifier()

router = APIRouter(
    prefix="/image_classification",
    tags=["Image Classification"],
)

@router.post("/")
def get_face_verification(selfie_image: UploadFile, profile_images: list[UploadFile]):
    return deepface_model.verify(selfie_image=selfie_image, profile_images=profile_images)

@router.post("/is_nsfw")
def is_nsfw(image: UploadFile):
    """
    Check if the image is NSFW (Not Safe For Work).

    Args:
        image (UploadFile): The image file to check.

    Returns:
        bool: True if the image is NSFW, False otherwise.
    """
    return deepface_model.is_nsfw(image=image.file.read())
