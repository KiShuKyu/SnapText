import keyboard
from capture.capture_region import capture_and_ocr


def trigger_capture():
    print("\n[!] Hotkey pressed! Starting SnapText...")
    try:
        capture_and_ocr()
        print("[+] Ready for next capture (Press Ctrl+Shift+F9)")
    except Exception as e:
        print(f"[-] Error during capture: {e}")


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
