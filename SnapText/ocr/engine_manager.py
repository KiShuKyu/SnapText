"""
ocr/engine_manager.py - EasyOCR engine loader with background warmup.

On start_warmup() the engine loads in a background thread so it is
ready before the first hotkey press. get_engine() blocks only if
warmup is still in progress when the hotkey is pressed.
"""

from __future__ import annotations

import threading
from ocr.engines.base import BaseOCREngine


class EngineManager:

    def __init__(self, languages: str) -> None:
        self._languages  = languages
        self._engine: BaseOCREngine | None = None
        self._lock       = threading.Lock()
        self._ready      = threading.Event()  # set when engine is loaded

    def start_warmup(self) -> None:
        """
        Begin loading the engine in a background thread immediately.
        Call this at startup so the engine is ready before first hotkey press.
        """
        t = threading.Thread(target=self._warmup_thread, daemon=True)
        t.start()

    def get_engine(self) -> BaseOCREngine:
        """
        Return the engine. If warmup is still running, blocks until done.
        If warmup was never started, loads synchronously now.
        """
        if not self._ready.is_set():
            if self._engine is None:
                # Warmup never started — load now
                self._load_engine()
            else:
                # Warmup in progress — wait for it
                print("[EngineManager] Waiting for engine warmup to finish...")
                self._ready.wait()

        return self._engine

    # ── Private ───────────────────────────────────────────────────────────────

    def _warmup_thread(self) -> None:
        print("[EngineManager] Background warmup started...")
        self._load_engine()
        print("[EngineManager] Engine ready — next capture will be fast.")

    def _load_engine(self) -> None:
        with self._lock:
            if self._engine is not None:
                return  # already loaded by another thread
            from ocr.engines.easyocr_engine import EasyOCREngine
            self._engine = EasyOCREngine(self._languages)
            self._ready.set()