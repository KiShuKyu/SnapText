from __future__ import annotations
import config


class CerebrasHelper:
    _PROMPT_ENGLISH = """\
You are correcting OCR output of English text.
Fix ONLY these specific OCR errors:
  - Merged words: "arejust" → "are just", "complainingabout" → "complaining about"
  - Wrong characters: 0/O confusion, 1/l/I confusion, rn/m confusion
  - Broken spacing and punctuation
Do NOT rephrase, summarise, or change meaning.
Return ONLY the corrected text, nothing else.

OCR Text:
{text}
"""

    _PROMPT_CODE = """\
You are correcting OCR output of source code.
Fix ONLY clear OCR character mistakes:
  - 0 vs O, 1 vs l vs I, rn vs m, ; vs :
  - Broken indentation (spaces/tabs misread)
  - Split identifiers: "my Var" → "myVar" if clearly one word
Preserve ALL syntax exactly — do not reformat, rename, or change logic.
Return ONLY the corrected code, nothing else.

OCR Text:
{text}
"""

    def __init__(self) -> None:
        self._client = None
        self._disabled = False

        if not config.CEREBRAS_API_KEY:
            print("[Cerebras] No API key — skipping.")
            return

        try:
            from cerebras.cloud.sdk import Cerebras
            # warm_tcp_connection=True reduces time-to-first-token
            self._client = Cerebras(api_key=config.CEREBRAS_API_KEY)
            print("[Cerebras] Client ready.")
        except Exception as exc:
            print(f"[Cerebras] Failed to initialise: {exc!r}")

    def clean_if_needed(self, text: str, confidence: float,
                        mode: str = "english") -> str:
        """
        Clean English or code text via Cerebras.

        Args:
            text:       Raw OCR output.
            confidence: Score from engine (0.0 – 1.0).
            mode:       "english" or "code"

        Returns:
            Cleaned text or original on skip/failure.
        """
        if not text.strip():
            return text
        if self._disabled:
            print("[Cerebras] Disabled for session — raw OCR used.")
            return text
        if confidence >= config.CEREBRAS_CONFIDENCE_THRESHOLD:
            return text
        if self._client is None:
            return text

        prompt = (
            self._PROMPT_CODE if mode == "code"
            else self._PROMPT_ENGLISH
        ).format(text=text)

        try:
            response = self._client.chat.completions.create(
                model=config.CEREBRAS_MODEL,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=1024,
                temperature=0.1,  # low temp = more deterministic corrections
            )
            result = response.choices[0].message.content
            if result:
                print(f"[Cerebras] Cleaned (conf={confidence:.2f}, mode={mode})")
                return result.strip()

        except Exception as exc:
            err = repr(exc).lower()
            if any(k in err for k in ("quota", "rate_limit", "429",
                                       "resource_exhausted", "limit")):
                print("[Cerebras] ⚠ Rate limit hit — disabling for session.")
                self._disabled = True
            else:
                print(f"[Cerebras] Cleanup failed: {exc!r}")

        return text

    @property
    def is_active(self) -> bool:
        return self._client is not None and not self._disabled