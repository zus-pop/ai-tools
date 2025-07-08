from fastapi import UploadFile, HTTPException
from deepface import DeepFace
import numpy as np
import cv2
import logging
import base64
from PIL import Image
import io
from transformers import pipeline

class ImageClassifier:
    logger = logging.getLogger(__name__)
    detector_backend: str = "retinaface"
    model_name: str = "Facenet512"
    def __init__(self):
        pass

    def _bytes_to_base64(self, data: bytes, content_type: str) -> str:
        """
        Convert bytes to base64 string.
        
        Args:
            data (bytes): The image data in bytes format.
            
        Returns:
            str: The image data as a base64 string.
        """
        encoded_image = base64.b64encode(data).decode('utf-8')
        return f"data:{content_type};base64,{encoded_image}"

    def _bytes_to_ndarray(self, data: bytes) -> np.ndarray:
        """ Convert bytes to a NumPy ndarray.
        Args:
            data (bytes): The image data in bytes format.
        Returns:
            np.ndarray: The image data as a NumPy ndarray.
        Raises:
            ValueError: If the image cannot be decoded.
        """
        self.logger.info(f"Converting bytes to ndarray")
        img_array = np.frombuffer(data, np.uint8)
        img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)  # BGR
        if img is None:
            raise ValueError("Cannot decode image bytes")
        return img

    
    def detect_faces(self, image_name: str, image_ndarray: np.ndarray) -> list[dict[str, any]]:
        """
        Detect faces in the given image.

        Args:
            image (UploadFile): The image file to process.

        Returns:
            list[dict[str, any]]: A list of dictionaries containing face detection results.
        """
        try:
            faces = DeepFace.extract_faces(
                    img_path=image_ndarray,
                    detector_backend=self.detector_backend,
                    anti_spoofing=True
            )
            return faces
        except Exception as e:
            self.logger.error(f"Error processing image {image_name}: {str(e)}")
            raise HTTPException(status_code=400, detail=f"The image {image_name} does not contain a human face or is not real.")

    def is_nsfw(self, image: bytes):
        """
        Check if the image is NSFW (Not Safe For Work).

        Args:
            image (UploadFile): The image file to check.

        Returns:
            bool: True if the image is NSFW, False otherwise.
        """
        img = Image.open(io.BytesIO(image))
        classifier = pipeline("image-classification", model="Falconsai/nsfw_image_detection")
        result = classifier(img)
        
        # Extract the classification results
        nsfw_result = None
        normal_result = None

        for item in result:
            if item['label'].lower() == 'nsfw':
                nsfw_result = item
            elif item['label'].lower() == 'normal':
                normal_result = item

        # Define threshold for NSFW detection
        nsfw_threshold = 0.8  # Adjust this value based on your requirements
        safe_threshold = 0.2   # Minimum normal score required

        # Determine if image is safe based on scores
        is_safe = True
        reason = "Image is safe"

        # Check individual thresholds first
        if nsfw_result['score'] > nsfw_threshold:
            is_safe = False
            reason = f"High NSFW content detected (score: {nsfw_result['score']:.3f})"
        elif normal_result['score'] < safe_threshold:
            is_safe = False
            reason = f"Low normal content score (score: {normal_result['score']:.3f})"
        else:
            # Optional: Additional relative check (you can remove this if too strict)
            # Only flag if NSFW score is more than 50% of normal score
            if nsfw_result['score'] > (normal_result['score'] * 0.5):
                is_safe = False
                reason = f"NSFW score concerning relative to normal score (NSFW: {nsfw_result['score']:.3f}, 50% Normal: {normal_result['score'] * 0.5:.3f})"
        
        return {
            "is_safe": is_safe,
            "reason": reason,
        }

    def verify(self, selfie_image: UploadFile, profile_images: list[UploadFile]):
        """
        Verify if the selfie image matches any of the profile images.

        Args:
            selfie_image (UploadFile): The selfie image to verify.
            profile_images (list[UploadFile]): List of profile images to compare against.

        Returns:
            dict: A dictionary containing the verification results.
        """
        current_image_name = ""
        selfie_image_bytes = selfie_image.file.read()
        self.logger.info(f"Processing selfie image {selfie_image.filename} with: {len(selfie_image_bytes)} bytes")

        is_nsfw_selfie_result = self.is_nsfw(selfie_image_bytes)
        if not is_nsfw_selfie_result["is_safe"]:
            raise HTTPException(status_code=400, detail=f"The selfie image is not safe for work: {is_nsfw_selfie_result['reason']}")
        
        selfie_ndarray = self._bytes_to_ndarray(selfie_image_bytes)
        # selfie_ndarray = self._bytes_to_base64(data=selfie_image_bytes, content_type=selfie_image.content_type)

        try:
            current_image_name = selfie_image.filename
            selfie_check = self.detect_faces(
                image_name=current_image_name,
                image_ndarray=selfie_ndarray
            )

            self.logger.info(f"The selfie image is {selfie_check[-1]['is_real']}")

            if (selfie_check[-1]["is_real"] is False):
                raise HTTPException(status_code=400, detail=f"The selfie image is not real or is spoofed or is not included with human face.")

            results = []
            for profile_image in profile_images:
                current_image_name = profile_image.filename
                profile_bytes = profile_image.file.read()
                self.logger.info(f"Processing profile image {profile_image.filename} with: {len(profile_bytes)} bytes")

                is_nsfw_profile_result = self.is_nsfw(profile_bytes)
                if not is_nsfw_profile_result["is_safe"]:
                    raise HTTPException(status_code=400, detail=f"The profile image {profile_image.filename} is not safe for work: {is_nsfw_profile_result['reason']}")

                # # Read the file contents as bytes
                profile_ndarray = self._bytes_to_ndarray(profile_bytes)
                # profile_ndarray = self._bytes_to_base64(data=profile_bytes, content_type=profile_image.content_type)

                profile_check = self.detect_faces(
                    image_name=current_image_name,
                    image_ndarray=profile_ndarray
                )

                self.logger.info(f"The profile image is {profile_check[-1]['is_real']}")

                if (profile_check[-1]["is_real"] is False):
                    raise HTTPException(status_code=400, detail=f"The profile image is not real or is spoofed or is not included with human face.")

                result = DeepFace.verify(
                    selfie_ndarray,
                    profile_ndarray,
                    model_name=self.model_name,
                    detector_backend=self.detector_backend,
                    align=True
                )
                results.append({
                    "profile_image": profile_image.filename,
                    "is_verified": result["verified"],
                    "distance": result["distance"],
                    "threshold": result["threshold"]
                })
            return results
        except Exception as e:
            self.logger.error(f"Error processing profile image {current_image_name}: {str(e)}")
            raise HTTPException(status_code=400, detail=f"Error processing profile image {current_image_name}: {str(e)}")