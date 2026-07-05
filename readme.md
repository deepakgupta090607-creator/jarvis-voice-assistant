# Jarvis Voice Assistant

A Python-based voice assistant with wake-word activation, web shortcuts, music playback, Wikipedia search, weather, news, app launching, AI chat, and system controls.

## Features
- Voice activation ("Jarvis") — say it once, then give commands continuously
- Open websites: Google, YouTube, GitHub, Instagram, Facebook, Claude, and more
- Open Windows apps: Notepad, Calculator, Chrome, VS Code, Word, Excel, etc.
- Close apps or the active window by voice
- Play any song (YouTube)
- Wikipedia search ("who is", "what is")
- Time & date
- Weather (no API key needed)
- News (general or topic/region specific)
- AI chat via Gemini
- Take photos / record videos via webcam
- Screenshot
- Volume control (Windows)
- File search and open
- Shutdown / restart PC
- Pause/resume listening ("stop" / "start")

## Setup

### 1. Install dependencies
```
pip install SpeechRecognition pyttsx3 pyaudio wikipedia-api requests
pip install pyautogui pycaw comtypes opencv-python
```

### 2. Set API keys as environment variables
This project needs two free API keys:
- **NewsAPI** — https://newsapi.org (free tier)
- **Gemini API** — https://ai.google.dev (free tier)

Set them as environment variables (never hardcode keys in the script):

**Windows (PowerShell):**
```
setx NEWS_API_KEY "your_key_here"
setx GEMINI_API_KEY "your_key_here"
```
Restart your terminal/VS Code after running these.

**macOS/Linux:**
```
export NEWS_API_KEY="your_key_here"
export GEMINI_API_KEY="your_key_here"
```

See `.env.example` for reference.

### 3. Edit custom app paths (optional)
Open `main.py` and update the `CUSTOM_APPS` dictionary with paths specific to your machine (e.g. PokiMMO, project folders).

### 4. Run
```
python main.py
```

Say **"Jarvis"** once to activate, then speak commands directly — no need to repeat the wake word.

## Notes
- Volume control and some app shortcuts are Windows-specific.
- Camera features require a free webcam and `opencv-python`.
- This is a personal/learning project — not production hardened.