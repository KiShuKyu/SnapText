"""
ocr/engines/base.py - Abstract base class for all OCR engines.

Every engine must implement read_text() and return (text, confidence).
confidence is a float in [0.0, 1.0] where 1.0 means fully confident.
"""

from __future__ import annotations

import numpy as np
from abc import ABC, abstractmethod


class BaseOCREngine(ABC):
    """Contract that all OCR engine adapters must satisfy."""

    def __init__(self, languages: str) -> None:
        self.languages = languages

    @abstractmethod
    def read_text(self, image: np.ndarray) -> tuple[str, float]:
        """
        Run OCR on a preprocessed image.

        Args:
            image: Grayscale or BGR uint8 NumPy array.

        Returns:
            (text, confidence) where confidence ∈ [0.0, 1.0].
        """