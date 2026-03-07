from __future__ import annotations

import numpy as np
from ocr.engines.base import BaseOCREngine

_LANG_MAP: dict[str, str] = {
    "eng": "en", "hin": "hi", "ben": "bn", "tam": "ta",
    "tel": "te", "mar": "mr", "guj": "gu", "kan": "kn",
    "mal": "ml", "urd": "ur", "chi_sim": "ch_sim",
    "chi_tra": "ch_tra", "jpn": "ja", "kor": "ko",
    "fra": "fr", "deu": "de", "spa": "es", "por": "pt",
    "ita": "it", "rus": "ru", "ara": "ar",
}


def _map_languages(lang_str: str) -> list[str]:
    langs = [l.strip() for l in lang_str.split("+") if l.strip()]
    mapped = [_LANG_MAP.get(l, l) for l in langs]
    seen, result = set(), []
    for lang in mapped:
        if lang not in seen:
            seen.add(lang)
            result.append(lang)
    return result


class EasyOCREngine(BaseOCREngine):

    def __init__(self, languages: str) -> None:
        super().__init__(languages)
        import easyocr
        lang_list = _map_languages(languages)
        print(f"[EasyOCREngine] Loading model for: {lang_list}")
        self._reader = easyocr.Reader(lang_list, verbose=False)
        print("[EasyOCREngine] Ready.")

    def read_text(self, image: np.ndarray) -> tuple[str, float]:
        results = self._reader.readtext(
            image,
            width_ths=0.3,        
            paragraph=False,      
            contrast_ths=0.1,    
            text_threshold=0.6,   
            decoder="greedy",     
            batch_size=8,         
        )

        if not results:
            return "", 0.0

        results = sorted(results, key=lambda r: (r[0][0][1], r[0][0][0]))

        text  = " ".join(r[1] for r in results)
        confs = [r[2] for r in results]
        return text.strip(), sum(confs) / len(confs)