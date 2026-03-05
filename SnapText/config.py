import os

OCR_LANG: str = os.getenv("OCR_LANG", "en+hi")

PREPROCESS_SCALE: float = float(os.getenv("PREPROCESS_SCALE", "1.5"))

CEREBRAS_API_KEY: str | None  = os.getenv("CEREBRAS_API_KEY")
CEREBRAS_MODEL: str           = os.getenv("CEREBRAS_MODEL", "llama-4-scout-17b-16e-instruct")
CEREBRAS_CONFIDENCE_THRESHOLD: float = float(
    os.getenv("CEREBRAS_CONFIDENCE_THRESHOLD", "0.75")
)

GEMINI_API_KEY: str | None  = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL: str           = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
USE_GEMINI: bool            = os.getenv("USE_GEMINI", "0") == "1"
GEMINI_CONFIDENCE_THRESHOLD: float = float(
    os.getenv("GEMINI_CONFIDENCE_THRESHOLD", "0.75")
)

HOTKEY: str = os.getenv("SNAPTEXT_HOTKEY", "ctrl+shift+f9")