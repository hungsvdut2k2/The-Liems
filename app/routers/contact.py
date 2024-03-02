import os
import pathlib
import uuid
from pydub import AudioSegment

from fastapi import APIRouter, HTTPException, UploadFile, Request, Query
from fuzzywuzzy import fuzz
from typing import List

router = APIRouter(prefix="/contact", tags=["Contact"])

@router.post("/audio")
async def audio_contact(audio: UploadFile, request: Request, contact_list: List[str] = Query(None)):
    file_extension = pathlib.Path(audio.filename).suffix
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
    scores = [fuzz.ratio(contact, text) for contact in contact_list]
    returned_contact = contact_list[scores.index(max(scores))]
    return {
        "text": text,
        "contact": returned_contact,
    }