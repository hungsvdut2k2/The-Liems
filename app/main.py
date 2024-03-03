import argparse
import pyrebase
import os

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from app.routers import auth, message, contact
from app.modules.image_captioning import ImageCaptioning
from app.modules.text_to_speech import TextToSpeech
from app.modules.speech_to_text import SpeechToText
from app.utils.userdatabase import UserDatabase

load_dotenv()
app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

firebaseConfig = {
    "apiKey": os.getenv("API_KEY"),
    "authDomain": os.getenv("AUTH_DOMAIN"),
    "databaseURL": os.getenv("DATABASE_URL"),
    "projectId": os.getenv("PROJECT_ID"),
    "storageBucket": os.getenv("STORAGE_BUCKET"),
    "messagingSenderId": os.getenv("MESSAGING_SENDER_ID"),
    "appId": os.getenv("APP_ID"),
    "measurementId": os.getenv("MEASUREMENT_ID"),
}

firebase = pyrebase.initialize_app(firebaseConfig)
app.authenticator = firebase.auth()
app.storage = firebase.storage()
app.database = firebase.database()
app.user_database = UserDatabase(app.database)
app.image_captioning = ImageCaptioning(model_name=os.getenv("IMAGE_CAPTIONING_MODEL"))
app.text_to_speech = TextToSpeech()
app.speech_to_text = SpeechToText()

app.include_router(auth.router)
app.include_router(message.router)
app.include_router(contact.router)


@app.get("/")
def root():
    return {"message": "Hello World"}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()
    uvicorn.run("main:app", host="0.0.0.0", port=args.port, reload=True)
