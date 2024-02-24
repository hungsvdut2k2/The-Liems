from typing import Optional

from gtts import gTTS


class TextToSpeech:
    def __init__(self):
        pass

    def convert_text_to_speech(
        self,
        message: Optional[str],
        language: Optional[str],
        save_file_path: Optional[str],
    ):
        tts = gTTS(text=message, lang=language)
        tts.save(save_file_path)
        return save_file_path
