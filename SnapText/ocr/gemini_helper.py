import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

client = None
if API_KEY:
    client = genai.Client(api_key=API_KEY)


def clean_ocr_text(text: str) -> str:
    """
    Post-process OCR output using Gemini.
    If Gemini is unavailable, returns original text.
    """

    if not text.strip():
        return text

    if client is None:
        # Graceful fallback
        return text

    prompt = f"""
You are given text extracted from OCR which may contain:
- Spelling errors
- Broken words
- Random line breaks
- OCR glyph mistakes

Instructions:
- Correct OCR mistakes only
- Preserve original language and script
- Do NOT translate
- Do NOT summarize
- Do NOT add new information
- Do NOT remove content

Return only the corrected text.

OCR TEXT:
{text}
"""

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.2,
            )
        )

        return response.text.strip()

    except Exception as e:
        print("Gemini correction failed:", e)
        return text