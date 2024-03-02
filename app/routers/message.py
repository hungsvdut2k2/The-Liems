import os
import pathlib
import uuid
from pydub import AudioSegment

from fastapi import APIRouter, HTTPException, UploadFile, Request
from PIL import Image
from transformers import AutoProcessor, BlipForConditionalGeneration
from typing import Optional

router = APIRouter(prefix="/message", tags=["Message"])

processor = AutoProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("hungsvdut2k2/image-captioning")


@router.post("/image")
async def image_captioning(
    file: UploadFile,
    request: Request,
):
    file_extension = pathlib.Path(file.filename).suffix
    storage = request.app.storage
    text2speech = request.app.text_to_speech
    if file_extension.lower() not in [".jpg", ".jpeg", ".png"]:
        raise HTTPException(
            status_code=400,
            detail="Invalid file format. Please upload a JPG or JPEG file.",
        )
    new_file_name = str(uuid.uuid4())

    file_location = f"./images/{new_file_name}.jpg"

    os.makedirs("./images", exist_ok=True)
    os.makedirs("./audios", exist_ok=True)
    with open(file_location, "wb+") as file_object:
        file_object.write(file.file.read())

    image = Image.open(file_location)
    pixel_values = processor(images=image, return_tensors="pt").pixel_values
    input_ids = model.generate(pixel_values=pixel_values, max_length=32)
    generate_text = processor.decode(input_ids[0], skip_special_tokens=True)
    audio_file_path = text2speech.convert_text_to_speech(
        message=generate_text,
        language="en",
        save_file_path=f"./audios/{new_file_name}.mp3",
    )

    storage.child(f"pictures/{new_file_name}.jpg").put(file_location)
    storage.child(f"audios/{new_file_name}.mp3").put(audio_file_path)

    return {
        "image_url": storage.child(f"pictures/{new_file_name}.jpg").get_url(None),
        "audio_url": storage.child(f"audios/{new_file_name}.mp3").get_url(None),
        "caption": generate_text,
    }


@router.post("/audio")
async def speech_to_text(
    audio: UploadFile,
    request: Request,
):
    file_extension = pathlib.Path(audio.filename).suffix
    storage = request.app.storage
    speech2text = request.app.speech_to_text
    if file_extension.lower() not in [".mp3"]:
        raise HTTPException(
            status_code=400,
            detail="Invalid file format. Please upload a MP3 file.",
        )
    new_file_name = str(uuid.uuid4())

    file_location = f"./audios/{new_file_name}.mp3"

    os.makedirs("./audios", exist_ok=True)
    with open(file_location, "wb+") as file_object:
        file_object.write(audio.file.read())

    wav_file_location = f"./audios/{new_file_name}.wav"
    sound = AudioSegment.from_mp3(file_location)
    sound.export(wav_file_location, format="wav")
    text = speech2text.convert_speech_to_text(wav_file_location)
    storage.child(f"audios/{new_file_name}.mp3").put(file_location)
    return {
        "text": text,
        "url": storage.child(f"audios/{new_file_name}.mp3").get_url(None),
    }
