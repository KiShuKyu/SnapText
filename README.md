# SnapText

https://github.com/user-attachments/assets/d3c91cff-aef9-4b0e-bd6c-31c301d498ff


SnapText is a modular, hotkey-driven **screen-to-text automation tool** built with Python. It allows users to select any region of the screen, extract text using OCR, clean and normalize that text with an LLM (Gemini API), and instantly copy the final result to the clipboard.

The project is designed with a **clean pipeline architecture** and a strong focus on reliability, correct dependency management, and extensibility. SnapText is fully functional up to a unified `main.py` entry point and demonstrated via a working demo video.

---

##  What SnapText Does

1. Trigger SnapText (currently via Python execution / hotkey mode)
2. Select a region on the screen (drag-to-select overlay)
3. Capture the selected region using OS-level APIs
4. Preprocess the image for better OCR accuracy
5. Extract text using Tesseract OCR
6. Clean and normalize OCR output using the Gemini API
7. Automatically copy the final text to the clipboard

This workflow turns screenshots into immediately usable text with minimal friction.

---

## 🧩 Architecture Overview

SnapText follows a **single-responsibility pipeline**, where each stage is isolated and testable:

```
Region Selection (Tkinter)
→ Screen Capture (MSS)
→ Image Preprocessing (OpenCV + NumPy)
→ OCR (Tesseract)
→ Text Cleanup / Normalization (Gemini API)
→ Clipboard Copy
```

This separation ensures clarity, debuggability, and ease of future upgrades.

---

## 📁 Project Structure

```
SnapText/
- ├── main.py                         # Application entry point
- │
- ├── capture/
- │   ├── __init__.py
- │   ├── region.py                   # Drag-to-select screen region
- │   ├── capture_region.py           # Capture selected region
- │   └── capture_screen.py           # Fullscreen capture (utility)
- │
- ├── ocr/
- │   ├── __init__.py
- │   └── gemini_helper.py            # Gemini API text cleanup
- │
- ├── .env                            # API keys (not committed)
- ├── .gitignore
- ├── README.md
```

---

## Tech Stack

* **Python 3.11** – stable interpreter choice for CV/OCR ecosystems
* **MSS** – fast, OS-level screen capture
* **Tkinter** – lightweight GUI overlay for region selection
* **OpenCV & NumPy** – image preprocessing to improve OCR accuracy
* **Tesseract OCR** – text extraction from images
* **Gemini API (google.genai)** – post-OCR text cleanup and normalization
* **pyperclip** – clipboard automation

---

## Python Version Note (Important)

SnapText intentionally uses **Python 3.11**.

This choice avoids binary compatibility issues between NumPy and OpenCV on Windows that can occur with newer Python versions. Pinning the interpreter ensures predictable behavior and a smoother development experience. This is standard practice in computer vision and OCR projects.

---

## Environment Setup

Gemini API credentials are stored securely using environment variables.

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_api_key_here
```

The `.env` file is ignored via `.gitignore` and is **not committed to GitHub**.

---

## Running the Project

From the `SnapText/` directory:

```bash
python main.py
```

A demo video is included in the repository showing the full workflow from region selection to clipboard copy.

---

## Packaging Status

SnapText is **not yet packaged as a standalone executable**.

* Current state: runnable via `main.py`
* Planned upgrade: Windows `.exe` packaging using PyInstaller

Packaging is intentionally deferred until the core functionality and UX are fully finalized.

---

## Future Improvements

* Package SnapText as a standalone desktop application (`.exe` / `.app`)
* Add system notifications ("Text copied")
* Introduce mode toggles (raw OCR / cleaned text / summary)
* Add background tray / hotkey-first operation
* Improve cross-platform hotkey handling (macOS, Linux)
* Optional OCR history logging

---

## Status

SnapText is **functionally complete up to a unified entry point (`main.py`)** and actively evolving. Core capture, OCR, AI cleanup, and clipboard automation are implemented and working as demonstrated.

---

## License

MIT License
