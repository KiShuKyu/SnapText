import mss
from PIL import Image
import time
import os

def capture_fullscreen():
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    filename = f"screenshot_{timestamp}.png"

    with mss.mss() as sct:
        monitor = sct.monitors[1]  # primary monitor
        shot = sct.grab(monitor)

        image = Image.frombytes(
            "RGB",
            shot.size,
            shot.rgb
        )

        image.save(filename)

    return filename


if __name__ == "__main__":
    saved_file = capture_fullscreen()
    print(f"Screenshot saved as: {os.path.abspath(saved_file)}")
