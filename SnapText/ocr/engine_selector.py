from .engines.tesseract_engine import TesseractEngine
from .engines.easyocr_engine import EasyOCREngine
from .engines.paddle_engine import PaddleEngine

def get_engine(name: str, lang: str):
    """
    name: "tesseract", "easyocr", "paddle"
    lang: language codes e.g. "en", "en+hi" (EasyOCR => ["en","hi"])
    """
    if name == "tesseract":
        return TesseractEngine(lang)

    elif name == "easyocr":
        langs = lang.split("+")
        return EasyOCREngine(langs)

    elif name == "paddle":
        # Paddle expects single code rather than list
        return PaddleEngine(lang)

    raise ValueError(f"OCR engine '{name}' is not supported")