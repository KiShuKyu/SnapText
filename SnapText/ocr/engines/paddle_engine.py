from paddleocr import PaddleOCR
from .base_engine import BaseOCREngine

class PaddleEngine(BaseOCREngine):

    def __init__(self, lang="en"):
        self.ocr = PaddleOCR(use_angle_cls=True, lang=lang)

    def read_text(self, image):
        result = self.ocr.ocr(image, cls=True)
        text = []
        for line in result:
            for word in line:
                text.append(word[1][0])
        return "\n".join(text)