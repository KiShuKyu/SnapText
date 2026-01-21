import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Load environment variables from .env
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise RuntimeError("GEMINI_API_KEY not found in environment variables.")

# Initialize Gemini client
client = genai.Client(api_key=API_KEY)


def clean_ocr_text(text: str) -> str:
    if not text.strip():
        return text

    prompt = f"""
You are given text extracted from OCR, which may contain spelling mistakes,
broken words, inconsistent formatting, or random line breaks.

Your task:
- Fix spelling and word breaks
- Preserve original meaning
- Improve readability
- Do NOT add new information
- Do NOT remove content

Return only the cleaned text.

OCR TEXT:
{text}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=0.2,
        )
    )

    return response.text.strip()
