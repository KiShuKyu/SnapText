import easyocr
from .base_engine import BaseOCREngine

class EasyOCREngine(BaseOCREngine):

    def __init__(self, languages=["en"]):
        self.reader = easyocr.Reader(languages)

    def read_text(self, image):
        results = self.reader.readtext(image)
        return "\n".join([r[1] for r in results])