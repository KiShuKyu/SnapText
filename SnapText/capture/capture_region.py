import cv2
import numpy as np
import mss
from .region import select_region

def capture_region():
    coords = select_region()  # returns (left, top, width, height)

    if coords is None:
        return None

    left, top, width, height = coords

    with mss.mss() as sct:
        monitor = {
            "left": left,
            "top": top,
            "width": width,
            "height": height,
        }
        screenshot = sct.grab(monitor)
        img = np.array(screenshot)
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
        return img