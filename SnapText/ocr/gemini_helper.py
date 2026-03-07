from __future__ import annotations
import config


class GeminiHelper:

    _PROMPT_HINDI = """\
You are correcting OCR output of Hindi (Devanagari) text.
Fix ONLY these specific OCR errors:
  - Merged words and broken matras (vowel signs)
  - Misread similar-looking Devanagari characters
  - Broken spacing between words
Preserve all Devanagari characters exactly — do not transliterate or translate.
Return ONLY the corrected Hindi text, nothing else.

OCR Text:
{text}
"""

    _PROMPT_MIXED = """\
You are correcting OCR output of mixed English and Hindi text.
Fix ONLY these specific OCR errors:
  - Merged English words: "arejust" → "are just"
  - Wrong characters in English: 0/O, 1/l/I, rn/m confusion
  - Broken Hindi matras and merged Hindi words
  - Broken spacing in both languages
Preserve all Devanagari characters exactly — do not transliterate or translate.
Do NOT rephrase or change meaning in either language.
Return ONLY the corrected text, nothing else.

OCR Text:
{text}
"""

    def __init__(self) -> None:
        self._client = None
        self._disabled = False

        if not config.GEMINI_API_KEY:
            print("[Gemini] No API key — Hindi cleanup disabled.")
            return

        try:
            from google import genai
            self._client = genai.Client(api_key=config.GEMINI_API_KEY)
            print("[Gemini] Client ready (Hindi + mixed mode).")
        except Exception as exc:
            print(f"[Gemini] Failed to initialise: {exc!r}")

    def clean_if_needed(self, text: str, confidence: float) -> str:
        #Only called when Devanagari script is detected.
        if not text.strip():
            return text
        if self._disabled:
            print("[Gemini] Disabled for session — raw OCR used.")
            return text
        if confidence >= config.GEMINI_CONFIDENCE_THRESHOLD:
            return text
        if self._client is None:
            return text

        has_latin = any("a" <= c.lower() <= "z" for c in text)
        prompt = (
            self._PROMPT_MIXED if has_latin else self._PROMPT_HINDI
        ).format(text=text)

        try:
            response = self._client.models.generate_content(
                model=config.GEMINI_MODEL,
                contents=prompt,
            )
            if response and response.text:
                print(f"[Gemini] Cleaned Hindi/mixed (conf={confidence:.2f})")
                return response.text.strip()

        except Exception as exc:
            err = repr(exc).lower()
            if any(k in err for k in ("quota", "resource_exhausted",
                                       "429", "rate_limit", "tokenlimit")):
                print("[Gemini] ⚠ Quota reached — disabling for session.")
                self._disabled = True
            else:
                print(f"[Gemini] Cleanup failed: {exc!r}")

        return text

    @property
    def is_active(self) -> bool:
        return self._client is not None and not self._disabled