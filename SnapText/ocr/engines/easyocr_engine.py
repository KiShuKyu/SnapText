import easyocr
from .base_engine import BaseOCREngine

class EasyOCREngine(BaseOCREngine):
    def __init__(self, languages):
        # expects list of language codes e.g. ["en","hi"]
        self.reader = easyocr.Reader(languages)

    def read_text(self, image):
        results = self.reader.readtext(image)
        return "\n".join([item[1] for item in results])