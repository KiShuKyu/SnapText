from __future__ import annotations

import pyperclip

import config
from app.hotkey import HotkeyListener
from app.notifier import notify
from capture.screen_capture import capture_region
from ocr.engine_manager import EngineManager
from ocr.preprocess import preprocess_image
from ocr.gemini_helper import GeminiHelper
from ui.region_selector import select_region


class Controller:

    def __init__(self) -> None:
        self._engine_manager = EngineManager(languages=config.OCR_LANG)
        self._gemini = GeminiHelper() if config.USE_GEMINI else None
        self._hotkey_listener = HotkeyListener(
            hotkey=config.HOTKEY,
            callback=self._on_hotkey,
        )

    def run(self) -> None:
        print(f"[SnapText] Ready. Press {config.HOTKEY} to capture.")
        print(f"[SnapText] Languages : {config.OCR_LANG}")
        print(f"[SnapText] Gemini    : {'enabled' if config.USE_GEMINI else 'disabled'}")

        self._engine_manager.start_warmup()

        notify("SnapText Running",
               f"Loading OCR engine in background...\nPress {config.HOTKEY} to capture.")

        self._hotkey_listener.start()

    def _on_hotkey(self) -> None:
        try:
            self._run_pipeline()
        except Exception as exc:
            print(f"[SnapText] Pipeline error: {exc!r}")
            notify("SnapText Error", str(exc), error=True)

    def _run_pipeline(self) -> None:
        region = select_region()
        if region is None:
            print("[SnapText] Cancelled.")
            return

        image = capture_region(region)
        if image is None:
            notify("Capture Failed", "Could not capture the selected region.", error=True)
            return

        processed = preprocess_image(image)

        engine = self._engine_manager.get_engine()
        text, confidence = engine.read_text(processed)
        print(f"[SnapText] OCR → '{text[:80]}{'…' if len(text) > 80 else ''}'  "
              f"(conf={confidence:.2f})")

        mode = _detect_mode(text)
        if self._gemini is not None:
            text = self._gemini.clean_if_needed(text, confidence, mode=mode)

        if text:
            pyperclip.copy(text)
            preview = text[:60] + ("…" if len(text) > 60 else "")
            gemini_note = ""
            if self._gemini and not self._gemini.is_active:
                gemini_note = "\n⚠ Gemini quota reached — raw OCR used."
            notify("Copied ✓", f"{preview}{gemini_note}")
            print("[SnapText] Copied to clipboard.")
        else:
            notify("Nothing Found",
                   "No text detected in the selected region.", error=True)


def _detect_mode(text: str) -> str:
    code_signals = [
        "def ", "class ", "import ", "return ", "if __",
        "function ", "const ", "var ", "let ", "=>",
        "#!/", "#include", "public static", "void ",
        "{", "}", "();", "[]", "->", "::", "==", "!=",
    ]
    hits = sum(1 for s in code_signals if s in text)
    return "code" if hits >= 2 else "general"