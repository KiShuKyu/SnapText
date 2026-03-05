from __future__ import annotations

import sys
from typing import Callable
import keyboard


class HotkeyListener:

    def __init__(self, hotkey: str, callback: Callable[[], None]) -> None:
        self._hotkey = hotkey
        self._callback = callback

    def start(self) -> None:
        keyboard.add_hotkey(self._hotkey, self._callback)
        print(f"[HotkeyListener] Listening on '{self._hotkey}' — right-click tray icon to quit.")
        try:
            keyboard.wait()
        except KeyboardInterrupt:
            print("\n[SnapText] Ctrl+C detected — shutting down.")
            keyboard.unhook_all()
            sys.exit(0)