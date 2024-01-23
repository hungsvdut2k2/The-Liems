import os
import pathlib
import uuid

from fastapi import APIRouter, HTTPException, UploadFile
from PIL import Image
from transformers import AutoProcessor, BlipForConditionalGeneration

router = APIRouter(prefix="/image", tags=["Images"])

processor = AutoProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("hungsvdut2k2/image-captioning")


@router.post("/captioning")
async def image_captioning(file: UploadFile):
    file_extension = pathlib.Path(file.filename).suffix
    if file_extension.lower() not in [".jpg", ".jpeg", ".png"]:
        raise HTTPException(
            status_code=400,
            detail="Invalid file format. Please upload a JPG or JPEG file.",
        )
    new_file_name = str(uuid.uuid4())

    file_location = f"./images/{new_file_name}.jpg"

    os.makedirs("./images", exist_ok=True)
    with open(file_location, "wb+") as file_object:
        file_object.write(file.file.read())

    image = Image.open(file_location)
    pixel_values = processor(images=image, return_tensors="pt").pixel_values
    input_ids = model.generate(pixel_values=pixel_values, max_length=32)
    return {"text": processor.decode(input_ids[0], skip_special_tokens=True)}
