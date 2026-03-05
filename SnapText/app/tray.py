from __future__ import annotations

import os
import sys
import threading
import keyboard
import config


def _make_icon():
    from PIL import Image, ImageDraw, ImageFont
    img  = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle([2, 2, 62, 62], radius=14, fill=(30, 58, 95))
    draw.text((20, 16), "S", fill=(255, 255, 255))
    return img


def _quit(icon, _item=None) -> None:
    """Clean shutdown — stops tray, unhooks keyboard, exits process."""
    print("[Tray] Shutting down SnapText...")
    try:
        icon.stop()
    except Exception:
        pass
    try:
        keyboard.unhook_all()
    except Exception:
        pass
    os._exit(0)   # hard exit — kills all threads including keyboard.wait()


def start_tray() -> None:
    """Start tray icon in background thread. Returns immediately."""
    try:
        import pystray
        from pystray import MenuItem, Menu

        icon_img = _make_icon()

        menu = Menu(
            MenuItem("SnapText", None, enabled=False),
            MenuItem(f"Hotkey: {config.HOTKEY}", None, enabled=False),
            MenuItem(f"Lang: {config.OCR_LANG}", None, enabled=False),
            MenuItem(
                f"Gemini: {'on' if config.USE_GEMINI else 'off'}",
                None, enabled=False,
            ),
            Menu.SEPARATOR,
            MenuItem("Quit SnapText", _quit),
        )

        icon = pystray.Icon("SnapText", icon_img, "SnapText", menu)

        threading.Thread(target=icon.run, daemon=True).start()
        print("[Tray] Running — right-click tray icon to quit.")

    except Exception as exc:
        print(f"[Tray] Could not start: {exc!r}")
        print("[Tray] Run: pip install pystray pillow")