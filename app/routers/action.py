import os
import pathlib
import uuid
import heapq

from fastapi import APIRouter, HTTPException, UploadFile, Request
from PIL import Image
from transformers import AutoProcessor, BlipForConditionalGeneration

from utils.utils import jaccard_similarity

router = APIRouter(prefix="/action", tags=["Action"])


@router.post("/searching")
async def switching(voice: UploadFile, quantity_output: int, request: Request):
    file_extension = pathlib.Path(voice.filename).suffix
    if file_extension.lower() not in [".mp3", ".mp4", ".wav"]:
        raise HTTPException(
            status_code=400,
            detail="Invalid file format. Please upload an MP3, MP4, or WAV file.",
        )

    new_file_name = str(uuid.uuid4())
    file_location = f"./actions/searching/{new_file_name}.mp3"
    with open(file_location, "wb") as f:
        f.write(await voice.read())

    speech2text = request.app.speech_to_text
    user_data = request.app.user_database

    emails = user_data.get_all_emails()
    user_request = speech2text.convert_speech_to_text(
        audio_file_path=file_location)

    similarly_score = {email: jaccard_similarity(
        email, user_request) for email in emails}
    retrieve_email = heapq.nlargest(
        quantity_output, similarly_score, key=similarly_score.get)
    return retrieve_email
