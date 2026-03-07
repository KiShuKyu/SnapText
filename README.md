# SnapText

> **Hotkey-driven screen-to-clipboard OCR for Windows.**
> Select any region on screen → text lands on your clipboard instantly.
> English and Hindi supported simultaneously. No switching required.

---

## Demo

https://github.com/user-attachments/assets/d3c91cff-aef9-4b0e-bd6c-31c301d498ff

---

## What It Does

Press `Ctrl+Shift+F9` from anywhere → drag a box over any text on screen → release.
That's it. The text is on your clipboard.

SnapText handles the entire pipeline automatically:
- Captures the selected region
- Preprocesses the image (handles dark mode, light mode, gradients)
- Extracts text using EasyOCR (English + Hindi simultaneously)
- Cleans and corrects the output using AI
- Copies to clipboard and shows a notification

---

## Features

- **English + Hindi OCR** — both languages loaded together, mixed content handled in one capture
- **Dual AI cleanup** — Cerebras for English/code (~200ms), Gemini for Hindi/mixed (~1-2s)
- **Smart routing** — automatically detects language and sends to the right AI
- **Code-aware** — detects source code and preserves syntax exactly
- **Dark mode support** — auto-detects dark/light backgrounds before processing
- **Background warmup** — OCR engine loads at startup, first capture is fast
- **System tray** — lives silently in taskbar, right-click to quit
- **Silent notifications** — toast on success, popup on error, no sound
- **Quota-safe** — if either AI hits its limit, falls back gracefully to raw OCR
- **Startup ready** — runs automatically on Windows login via Task Scheduler

---

## Pipeline

Every hotkey press runs this sequence:

```
Hotkey pressed (ctrl+shift+f9)
        │
        ▼
region_selector      Tkinter full-screen overlay — user drags a box
        │            Returns (left, top, width, height)
        ▼
screen_capture       mss grabs that exact region → NumPy BGR array
        │
        ▼
preprocess           Grayscale → Denoise → Smart scale →
                     Auto dark/light detect → Adaptive threshold → Sharpen
        │
        ▼
EasyOCR              Reads text + confidence score (0.0 – 1.0)
        │
        ▼
Smart LLM routing    controller scans for Devanagari characters
        │
        ├── Hindi / Mixed (हिंदी detected)
        │       └── Gemini 2.5 Flash  (~1-2 sec, better Devanagari)
        │               ├── Pure Hindi   → Hindi prompt
        │               └── Mixed en+hi  → Mixed prompt
        │
        └── English / Code (no Devanagari)
                └── Cerebras llama-4-scout  (~200ms, free)
                        ├── Code detected   → Code prompt (preserves syntax)
                        └── Plain English   → English prompt
        │
        ▼
pyperclip            Text copied to clipboard
        │
        ▼
notifier             Toast notification with text preview
```

---

## Architecture

```
SnapText/
│
├── main.py                   Bootstrap — loads .env, starts tray + controller
├── config.py                 All settings in one place
│
├── app/
│   ├── controller.py         Pipeline orchestrator + LLM routing logic
│   ├── hotkey.py             Global keyboard listener
│   ├── notifier.py           Toast (success) + popup (error) notifications
│   └── tray.py               System tray icon with quit menu
│
├── ui/
│   └── region_selector.py    Tkinter drag-to-select overlay
│
├── capture/
│   └── screen_capture.py     mss screen region capture
│
└── ocr/
    ├── engine_manager.py     Lazy loader with background warmup thread
    ├── preprocess.py         Smart image preprocessing pipeline
    ├── cerebras_helper.py    Cerebras cleanup — English + code
    ├── gemini_helper.py      Gemini cleanup — Hindi + mixed
    └── engines/
        ├── base.py           Abstract engine interface
        └── easyocr_engine.py EasyOCR adapter (en+hi, tuned parameters)
```

### Why Two AI Helpers?

Each helper has one job and owns its own API client, prompts, and error handling.
`controller.py` is the only place that knows both exist and decides which to call.

| Helper | Handles | Model | Speed |
|---|---|---|---|
| `cerebras_helper.py` | English, Code | llama-4-scout-17b | ~200ms |
| `gemini_helper.py` | Hindi, Mixed en+hi | gemini-2.5-flash | ~1-2s |

If Cerebras is unavailable or has no API key, controller falls back to Gemini for English too — nothing breaks.

---

## Tech Stack

| Library | Purpose |
|---|---|
| EasyOCR | Deep learning OCR — English + Hindi |
| PyTorch | Neural network backend for EasyOCR |
| OpenCV + NumPy | Image preprocessing |
| mss | Fast OS-level screen capture |
| Tkinter | Drag-to-select overlay (built into Python) |
| keyboard | Global hotkey listener |
| Cerebras SDK | Fast LLM cleanup — English + code |
| Google Generative AI | LLM cleanup — Hindi + mixed |
| pystray + Pillow | System tray icon |
| win10toast / plyer | Silent Windows toast notifications |
| pyperclip | Clipboard automation |
| python-dotenv | Environment variable loading |

---

## Setup

```bash
# 1. Clone
git clone https://github.com/KiShuKyu/SnapText
cd SnapText/SnapText

# 2. Create virtual environment — Python 3.11 recommended
py -3.11 -m venv .venv
.venv\Scripts\Activate.ps1

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure
copy .env.example .env
# Add your API keys (see Configuration below)

# 5. Run
python main.py
```

---

## Configuration (`.env`)

```env
# Languages — en+hi = English and Hindi loaded simultaneously
OCR_LANG=en+hi

# Cerebras — English + code cleanup (~200ms, free tier available)
# Get key at: cloud.cerebras.ai
CEREBRAS_API_KEY=your_cerebras_key_here
CEREBRAS_MODEL=llama-4-scout-17b-16e-instruct
CEREBRAS_CONFIDENCE_THRESHOLD=0.75

# Gemini — Hindi + mixed cleanup
# Get key at: aistudio.google.com
USE_GEMINI=1
GEMINI_API_KEY=your_gemini_key_here
GEMINI_MODEL=gemini-2.5-flash
GEMINI_CONFIDENCE_THRESHOLD=0.75

# Preprocessing scale (1.5 = auto smart scaling)
PREPROCESS_SCALE=1.5

# Hotkey
SNAPTEXT_HOTKEY=ctrl+shift+f9
```

### Tuning tips

| Setting | Value | Effect |
|---|---|---|
| `PREPROCESS_SCALE` | `2.0` | Better for small text (tooltips, status bars) |
| `CEREBRAS_CONFIDENCE_THRESHOLD` | `0.90` | Cerebras runs more often |
| `GEMINI_CONFIDENCE_THRESHOLD` | `0.90` | Gemini runs more often |
| `OCR_LANG` | `en` | English only, faster model load |
| `USE_GEMINI` | `0` | Disable Gemini, use Cerebras for everything |

---

## Supported Languages

To add more languages update `OCR_LANG` in `.env` using `+` to combine:

| Language | Code | Language | Code |
|---|---|---|---|
| English | `en` | Tamil | `ta` |
| Hindi | `hi` | Telugu | `te` |
| Bengali | `bn` | Marathi | `mr` |
| Gujarati | `gu` | Kannada | `kn` |
| Malayalam | `ml` | Urdu | `ur` |

Example: `OCR_LANG=en+hi+bn` for English + Hindi + Bengali

> **Note:** Each additional language adds ~100MB model download on first run and increases RAM usage. Recommended maximum: 2 languages.

---

## Running at Startup (Windows)

1. Open **Task Scheduler** → **Create Basic Task**
2. **Trigger** → When I log on
3. **Action** → Start a program
   - Program: `D:\path\to\SnapText\.venv\Scripts\pythonw.exe`
   - Arguments: `D:\path\to\SnapText\SnapText\main.py`
   - Start in: `D:\path\to\SnapText\SnapText`
4. After creating → Properties → **Triggers** → Edit → Delay **30 seconds**
5. **General** tab → Run only when user is logged on

To restart manually: right-click the task → **Run**, or double-click a desktop shortcut pointing to `pythonw.exe main.py`.

---

## Python Version Note

SnapText uses **Python 3.11**. This avoids binary compatibility issues between NumPy, OpenCV, and PyTorch on Windows that appear with newer versions. Standard practice for CV/OCR projects.

---

## Roadmap

- [ ] PaddleOCR engine for Chinese / Japanese / Korean
- [ ] OCR history log with timestamps
- [ ] More language pairs
- [ ] Standalone `.exe` packaging (post feature-complete)

---

## License

MIT License