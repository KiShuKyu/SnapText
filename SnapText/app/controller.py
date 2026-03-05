from __future__ import annotations
import pyperclip
import config
from app.hotkey import HotkeyListener
from app.notifier import notify
from capture.screen_capture import capture_region
from ocr.engine_manager import EngineManager
from ocr.preprocess import preprocess_image
from ocr.cerebras_helper import CerebrasHelper
from ocr.gemini_helper import GeminiHelper
from ui.region_selector import select_region


class Controller:

    def __init__(self) -> None:
        self._engine_manager = EngineManager(languages=config.OCR_LANG)

        # Dual LLM setup
        self._cerebras = CerebrasHelper() if config.CEREBRAS_API_KEY else None
        self._gemini   = GeminiHelper()   if config.GEMINI_API_KEY   else None

        self._hotkey_listener = HotkeyListener(
            hotkey=config.HOTKEY,
            callback=self._on_hotkey,
        )

    def run(self) -> None:
        print(f"[SnapText] Ready. Press {config.HOTKEY} to capture.")
        print(f"[SnapText] Languages : {config.OCR_LANG}")
        print(f"[SnapText] Cerebras  : {'enabled' if self._cerebras else 'no key'}")
        print(f"[SnapText] Gemini    : {'enabled' if self._gemini else 'no key'}")

        self._engine_manager.start_warmup()

        notify("SnapText Running",
               f"Loading OCR in background...\nPress {config.HOTKEY} to capture.")

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

        text = self._route_cleanup(text, confidence)

        if text:
            pyperclip.copy(text)
            preview = text[:60] + ("…" if len(text) > 60 else "")
            notify("Copied ✓", preview)
            print("[SnapText] Copied to clipboard.")
        else:
            notify("Nothing Found",
                   "No text detected in the selected region.", error=True)

    def _route_cleanup(self, text: str, confidence: float) -> str:
        if not config.USE_GEMINI and not config.CEREBRAS_API_KEY:
            return text  # both disabled — return raw OCR

        has_devanagari = any("\u0900" <= c <= "\u097F" for c in text)
        mode = _detect_mode(text)

        if has_devanagari:
            # Hindi or mixed — use Gemini
            if self._gemini:
                return self._gemini.clean_if_needed(text, confidence)
            return text
        else:
            # English or code — use Cerebras
            if self._cerebras:
                return self._cerebras.clean_if_needed(text, confidence, mode=mode)
            # Fallback to Gemini if no Cerebras key
            if self._gemini:
                return self._gemini.clean_if_needed(text, confidence)
            return text


def _detect_mode(text: str) -> str:
    """Detect if text looks like source code."""
    code_signals = [
        "def ", "class ", "import ", "return ", "if __",
        "function ", "const ", "var ", "let ", "=>",
        "#!/", "#include", "public static", "void ",
        "{", "}", "();", "[]", "->", "::", "==", "!=",
    ]
    hits = sum(1 for s in code_signals if s in text)
    return "code" if hits >= 2 else "english"