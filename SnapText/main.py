import keyboard
from capture.capture_region import preprocess_image
from ocr.engine_selector import get_engine
from capture.capture_region import capture_region

# initialize engine ONCE
# choose engine and languages here:
USE_GEMINI = True
text = ocr_engine.read_text(processed)

if USE_GEMINI:
    from ocr.gemini_helper import clean_ocr_text
    text = clean_ocr_text(text)

ocr_engine = get_engine("easyocr", "en+hi")

def perform_capture():
    # 1. capture
    raw_img = capture_and_ocr()

    # 2. preprocess
    processed = preprocess_image(raw_img)

    # 3. run through selected OCR engine
    text = ocr_engine.read_text(processed)

    print("\n=== OCR OUTPUT ===")
    print(text)
    print("==================")

def trigger_capture(raw_img):
    print("[!] Hotkey pressed — capturing...")
    try:
        perform_capture()
        print("[+] Done.")
        print("Ready for next (Press Ctrl+Shift+F9)")
    except Exception as e:
        print("[-] Error:", e)

# register global hotkey
keyboard.add_hotkey("ctrl+shift+f9", trigger_capture)

print("SnapText OCR ready. Press Ctrl+Shift+F9.")

keyboard.wait()