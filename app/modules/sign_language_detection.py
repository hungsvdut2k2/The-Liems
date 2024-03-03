from typing import Optional

from PIL import Image
from transformers import AutoProcessor, BlipForConditionalGeneration
from ultralytics import YOLO

class SignLanguageDetection:
    RESULTS_MAPPING = {
        0: 'A', 1: 'B', 2: 'C',
        3: 'D', 4: 'E', 5: 'F',
        6: 'G', 7: 'H', 8: 'I',
        9: 'J', 10: 'K', 11: 'L',
        12: 'M', 13: 'N', 14: 'O',
        15: 'P', 16: 'Q', 17: 'R',
        18: 'S', 19: 'T', 20: 'U',
        21: 'V', 22: 'W', 23: 'X',
        24: 'Y', 25: 'Z'
    }

    def __init__(self, model_path: Optional[str]) -> None:
        self.model = YOLO(model_path)

    def recognizing(self, image_path: Optional[str]) -> str:
        output = self.model(image_path)[0].boxes.cls
        output = output.item()
        return self.RESULTS_MAPPING[output]
    
if __name__ == '__main__':
    sld = SignLanguageDetection('/home/link/spaces/The-Liems/models/slr.pt')
    result = sld.recognizing(
        '/home/link/spaces/The-Liems/slr/American-Sign-Language-Letters-1/test/images/F3_jpg.rf.c854e14a7108c9294c226a392026e73b.jpg')
    print(result)