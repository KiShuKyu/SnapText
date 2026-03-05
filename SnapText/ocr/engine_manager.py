from .engines.tesseract_engine import TesseractEngine
from .engines.easyocr_engine import EasyOCREngine
from .engines.paddle_engine import PaddleEngine

def get_engine(name: str, languages: str):
    name = name.lower()
    if name == "tesseract":
        return TesseractEngine(languages)
    if name == "easyocr":
        return EasyOCREngine(languages)
    if name == "paddle":
        return PaddleEngine(languages)
    raise ValueError(f"Unknown OCR engine: {name}")