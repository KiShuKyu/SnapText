import pytesseract
from .base_engine import BaseOCREngine

class TesseractEngine(BaseOCREngine):
    def __init__(self, lang="eng"):
        self.lang = lang

    def read_text(self, image):
        custom_config = r"--oem 3 --psm 6"
        text = pytesseract.image_to_string(
            image, lang=self.lang, config=custom_config
        )
        return text