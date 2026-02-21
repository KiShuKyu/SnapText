from engines.tesseract_engine import TesseractEngine
from engines.easyocr_engine import EasyOCREngine
from engines.paddle_engine import PaddleEngine

def get_engine(name, lang):

    if name == "tesseract":
        return TesseractEngine(lang)

    elif name == "easyocr":
        return EasyOCREngine(lang.split("+"))

    elif name == "paddle":
        return PaddleEngine(lang)

    else:
        raise ValueError("Unknown OCR engine")