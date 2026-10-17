# PyCalc — Python mobile calculator

A small calculator built with Python and Kivy. It can be previewed on a desktop and packaged as an Android APK.

## Features
- Addition, subtraction, multiplication and division
- Decimal numbers, clear, delete, sign toggle and percentage
- Error handling for invalid expressions and division by zero
- Simple dark interface

## 1. Run locally (Windows)

Use Python 3.10 or 3.11 for a straightforward first test.

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install kivy
python main.py
```

If `py -3.11` is unavailable, use a Python version installed on your computer and supported by the Kivy release you install.

## 2. Build an Android APK

Kivy recommends Buildozer for Android packaging. Buildozer's Android toolchain runs on Linux or macOS; on Windows, use WSL2 with Ubuntu.

Inside Ubuntu/WSL, install the system dependencies following the current official guide:
https://buildozer.readthedocs.io/en/stable/installation.html

Then, from this project directory:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install kivy buildozer
buildozer init
```

Edit `buildozer.spec` and set at least:
- `title = PyCalc`
- `package.name = pycalc`
- `package.domain = org.example`
- `source.include_exts = py,kv,png,jpg,atlas`
- `requirements = python3,kivy`

Build the debug APK:

```bash
buildozer -v android debug
```

The APK is normally created in the `bin/` directory. Transfer it to your Android phone and install it, allowing installation from that source if Android asks.

## Important limitations
- The first Android build can take a while because SDK/NDK dependencies are downloaded.
- This project source is provided; an APK has not been built or tested on a physical phone in this environment.
- For iOS, packaging generally requires macOS and Apple's Xcode toolchain.

## Official references
- Kivy Android packaging: https://kivy.org/doc/stable/guide/packaging-android.html
- Buildozer quickstart: https://buildozer.readthedocs.io/en/stable/quickstart.html
