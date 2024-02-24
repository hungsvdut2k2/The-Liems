import speech_recognition as sr
from typing import Optional


class SpeechToText:
    def __init__(self) -> None:
        self.recognizer = sr.Recognizer()

    def convert_speech_to_text(self, audio_file_path: Optional[str]) -> str:
        with sr.AudioFile(audio_file_path) as source:
            audio = self.recognizer.record(source)
            return self.recognizer.recognize_google(audio)
