from typing import Optional

from PIL import Image
from transformers import AutoProcessor, BlipForConditionalGeneration


class ImageCaptioning:
    def __init__(self, model_name: Optional[str]) -> None:
        self.processor = AutoProcessor.from_pretrained(model_name)
        self.model = BlipForConditionalGeneration.from_pretrained(model_name)

    def generate_caption(self, image_path: Optional[str]) -> str:
        image = Image.open(image_path)
        pixel_values = self.processor(images=image, return_tensors="pt").pixel_values
        input_ids = self.model.generate(pixel_values=pixel_values, max_length=32)
        return self.processor.decode(input_ids[0], skip_special_tokens=True)
