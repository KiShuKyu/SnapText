from __future__ import annotations

import cv2
import numpy as np
import config

TARGET_WIDTH = 1200   # px — optimal input size for EasyOCR
MIN_SCALE    = 1.0    
MAX_SCALE    = 3.0    


def preprocess_image(image: np.ndarray) -> np.ndarray:

    if image.ndim == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image.copy()

    gray = cv2.fastNlMeansDenoising(gray, h=10)

    if config.PREPROCESS_SCALE > 1.5:
        scale = config.PREPROCESS_SCALE
    else:
        h, w  = gray.shape
        scale = TARGET_WIDTH / w if w < TARGET_WIDTH else 1.0
        scale = max(MIN_SCALE, min(MAX_SCALE, scale))

    if scale != 1.0:
        gray = cv2.resize(
            gray, None, fx=scale, fy=scale,
            interpolation=cv2.INTER_CUBIC,
        )

    if np.mean(gray) < 128:
        gray = cv2.bitwise_not(gray)


    thresh = cv2.adaptiveThreshold(
        gray, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        blockSize=15,
        C=4,
    )

    blurred = cv2.GaussianBlur(thresh, (0, 0), 1.0)
    sharp   = cv2.addWeighted(thresh, 1.5, blurred, -0.5, 0)

    return sharp