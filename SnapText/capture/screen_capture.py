from __future__ import annotations

import numpy as np


def capture_region(
    region: tuple[int, int, int, int],
) -> np.ndarray | None:
    import mss  # local import — no mss context alive until needed

    left, top, width, height = region
    if width <= 0 or height <= 0:
        return None

    monitor = {"left": left, "top": top, "width": width, "height": height}

    try:
        with mss.mss() as sct:
            screenshot = sct.grab(monitor)
            # mss gives BGRA; drop alpha channel → BGR for OpenCV
            frame = np.array(screenshot)
            return frame[:, :, :3]
    except Exception as exc:
        print(f"[capture] mss error: {exc!r}")
        return None