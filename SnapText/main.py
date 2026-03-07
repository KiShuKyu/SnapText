import os
import sys
import warnings


warnings.filterwarnings("ignore", message=".*pin_memory.*", category=UserWarning)

from dotenv import load_dotenv
load_dotenv()

os.environ.setdefault("PADDLE_PDX_DISABLE_MODEL_SOURCE_CHECK", "True")

if __name__ == "__main__":
    from app.tray import start_tray
    from app.controller import Controller

    start_tray()

    ctrl = Controller()
    ctrl.run()