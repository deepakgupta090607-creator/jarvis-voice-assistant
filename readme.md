# 🎙️ Jarvis Voice Assistant

A Python-based desktop voice assistant with wake-word activation, web shortcuts, music playback, Wikipedia search, weather, news, AI chat, camera controls, and system automation — all controlled entirely by voice.

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey?logo=windows)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Active-brightgreen)

---

## ✨ Features

| Category | What it does |
|---|---|
| 🎤 **Wake word** | Say **"Jarvis"** once to activate — no need to repeat it before every command |
| 🌐 **Web shortcuts** | Open Google, YouTube, GitHub, Instagram, Facebook, Claude, ChatGPT, and more by voice |
| 🖥️ **App control** | Open or close Notepad, Calculator, Chrome, VS Code, Word, Excel, Task Manager, etc. |
| 🎵 **Music** | Play any song — searches and plays the top YouTube result directly |
| 📖 **Wikipedia** | Ask "who is..." or "what is..." for instant summaries |
| ⏰ **Time & Date** | Get the current time or date |
| 🌦️ **Weather** | Live weather for any city (no API key required) |
| 📰 **News** | General headlines or topic/region-specific news, with AI fallback if nothing is found |
| 🤖 **AI Chat** | Ask Jarvis anything — powered by Google Gemini |
| 📸 **Camera** | Take photos or record short videos from your webcam |
| 🖼️ **Screenshot** | Capture and save your screen instantly |
| 🔊 **Volume control** | Increase, decrease, mute, or unmute system volume |
| 📁 **File search** | Find and open any file on your system by name |
| 🔌 **System control** | Shutdown or restart your PC by voice |
| ⏸️ **Pause / Resume** | Say "stop" to pause listening, "start" to resume — without closing the app |

---

## 🛠️ Tech Stack

- **Speech Recognition** — [`SpeechRecognition`](https://pypi.org/project/SpeechRecognition/) (Google Speech API)
- **Text-to-Speech** — [`pyttsx3`](https://pypi.org/project/pyttsx3/)
- **Wikipedia** — [`wikipedia-api`](https://pypi.org/project/Wikipedia-API/)
- **Weather** — [Open-Meteo](https://open-meteo.com/) (free, no key)
- **News** — [NewsAPI](https://newsapi.org/)
- **AI Chat** — [Google Gemini API](https://ai.google.dev/)
- **Camera** — [`opencv-python`](https://pypi.org/project/opencv-python/)
- **Volume Control** — [`pycaw`](https://pypi.org/project/pycaw/)
- **Automation** — [`pyautogui`](https://pypi.org/project/pyautogui/)

---

## 📋 Prerequisites

- Python 3.11 (recommended)
- Windows OS (some features like volume control and shutdown/restart are Windows-specific)
- A working microphone
- Internet connection (for speech recognition, weather, news, and AI features)

---

## 🚀 Installation

**1. Clone the repository**
```bash
git clone https://github.com/deepakgupta090607-creator/jarvis-voice-assistant.git
cd jarvis-voice-assistant
```

**2. Install dependencies**
```bash
pip install SpeechRecognition pyttsx3 pyaudio wikipedia-api requests
pip install pyautogui pycaw comtypes opencv-python
```

> **Note:** If `pyaudio` fails to install on Windows, use:
> ```bash
> pip install pipwin
> pipwin install pyaudio
> ```

**3. Set up API keys**

This project uses two free API keys. Copy `.env.example` for reference and set these as environment variables (never hardcode keys in the script):

| Variable | Get it from |
|---|---|
| `NEWS_API_KEY` | [newsapi.org](https://newsapi.org) (free tier) |
| `GEMINI_API_KEY` | [ai.google.dev](https://ai.google.dev) (free tier) |

**Windows (PowerShell):**
```powershell
setx NEWS_API_KEY "your_key_here"
setx GEMINI_API_KEY "your_key_here"
```
Restart your terminal/VS Code after running these so the variables load.

**macOS/Linux:**
```bash
export NEWS_API_KEY="your_key_here"
export GEMINI_API_KEY="your_key_here"
```

**4. Configure custom apps (optional)**

Open `main.py` and edit the `CUSTOM_APPS` dictionary with paths specific to your machine (e.g. games, project folders):
```python
CUSTOM_APPS = {
    "ai voice": r"e:\ai voice",
    "pokimmo": r"D:\PS3\PokeMMO\PokeMMO.exe",
}
```

---

## ▶️ Usage

```bash
python main.py
```

1. Wait for **"Jarvis is ready"**
2. Say **"Jarvis"** once to activate
3. Speak commands directly — no need to repeat the wake word

### Example commands
```
"open youtube"
"play kesariya"
"who is Albert Einstein"
"what's the weather in Chandigarh"
"weather in Amritsar"
"punjab news"
"take a photo"
"volume up"
"close chrome"
"open file resume"
"stop"        → pauses listening
"start"       → resumes listening
"exit"        → closes the program
```

---

## 📂 Project Structure

```
jarvis-voice-assistant/
├── main.py            # Main assistant script
├── .env.example       # Reference for required environment variables
├── .gitignore
└── README.md
```

---

## ⚠️ Notes & Limitations

- Volume control, shutdown/restart, and some app shortcuts are **Windows-only**.
- Camera features require a working webcam and `opencv-python`.
- Closing browser tabs (e.g. "close youtube") isn't possible — only whole applications or the active window can be closed.
- News answers fall back to AI-generated summaries when no live articles are found, so they may not always reflect breaking news.
- This is a personal/learning project, not hardened for production use.

---

## 🤝 Contributing

This is a personal project built for learning, but suggestions and pull requests are welcome. Feel free to open an issue if you find a bug.

---

## 📄 License

This project is open source and available under the MIT License.

---

## 🙋 Author


**Deepak Gupta**
B.E. Computer Science Engineering, Chitkara University