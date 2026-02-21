import keyboard
from capture.capture_region import capture_and_ocr
from capture.capture_region import preprocess_image
import pytesseract
from ocr.engine_selector import get_engine

image = capture_and_ocr()
processed = preprocess_image(image)
# text = engine.read_text(processed_image)
#



# custom_config = r'--oem 3 --psm 6'
# text = pytesseract.image_to_string(
#     processed,
#     lang='eng',
#     config=custom_config
# )



from capture.capture_region import capture_region
from ocr.preprocess import preprocess_image
from ocr.engine_selector import get_engine

engine = get_engine("easyocr", "en+hi")

def trigger_capture():
    image = capture_region()
    processed = preprocess_image(image)
    text = engine.read_text(processed)
    print(text)
def main():
    hotkey = 'ctrl+shift+F9'

    print(f"--- SnapText Background Service ---")
    print(f"Hotkey: Press {hotkey.upper()} to capture text.")
    print(f"Exit:   Press ESC to close the application.")
    print("-" * 35)

    # Register the hotkey
    keyboard.add_hotkey(hotkey, trigger_capture)
    keyboard.wait('esc')
    print("\n[!] SnapText closed.")

if __name__ == "__main__":
    main()
