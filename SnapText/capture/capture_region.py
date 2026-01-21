import time
import mss
from PIL import Image
import pytesseract
import cv2
import numpy as np
import pyperclip
from SnapText.capture.region import RegionSelector
from SnapText.ocr.gemini_helper import clean_ocr_text

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def preprocess_image(pil_image):
    """
    Tuned preprocessing for hard screenshots.
    Returns a PIL Image optimized for OCR.
    """

    # Convert PIL → NumPy
    img = np.array(pil_image)

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    # Resize up (OCR likes bigger text)
    gray = cv2.resize(
        gray,
        None,
        fx=1.5,
        fy=1.5,
        interpolation=cv2.INTER_CUBIC
    )

    # Reduce noise slightly (helps thresholding)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)

    # Adaptive threshold (handles uneven lighting)
    thresh = cv2.adaptiveThreshold(
        gray,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        11,
        2
    )

    # Morphological cleanup
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
    thresh = cv2.morphologyEx(
        thresh,
        cv2.MORPH_CLOSE,
        kernel
    )

    # Return to PIL for Tesseract
    return Image.fromarray(thresh)



def capture_and_ocr():
    selector = RegionSelector()
    region = selector.select()

    if region is None:
        print("Selection cancelled.")
        return

    left, top, width, height = region

    with mss.mss() as sct:
        monitor = {
            "left": left,
            "top": top,
            "width": width,
            "height": height
        }
        shot = sct.grab(monitor)
        original_image = Image.frombytes("RGB", shot.size, shot.rgb)

    # 🔹 NEW STEP: Preprocess image using OpenCV
    processed_image = preprocess_image(original_image)
    raw_text = pytesseract.image_to_string(processed_image)

    clean_text = clean_ocr_text(raw_text)

    if clean_text.strip():
        pyperclip.copy(clean_text)
        print("Cleaned text copied to clipboard.")
    else:
        print("No text detected.")

        # Optional: save OCR output
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    # text_file = f"ocr_text_{timestamp}.txt"

    # with open(text_file, "w", encoding="utf-8") as f:
    #     f.write(text)

    print("OCR complete.")
    # print("Saved text to:", os.path.abspath(text_file))
    print("\nExtracted text:\n")
    print(clean_text)

if __name__ == "__main__":
    capture_and_ocr()
