from paddleocr import PaddleOCR
from .base_engine import BaseOCREngine

class PaddleEngine(BaseOCREngine):
    def __init__(self, lang="en"):
        # example: lang="en" or lang="hi" etc.
        self.ocr = PaddleOCR(use_angle_cls=True, lang=lang)

    def read_text(self, image):
        results = self.ocr.ocr(image, cls=True)
        lines = []
        for line in results:
            for word in line:
                lines.append(word[1][0])
        return "\n".join(lines)