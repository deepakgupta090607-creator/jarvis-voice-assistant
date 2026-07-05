"""
Jarvis Voice Assistant
----------------------
A voice-activated desktop assistant with web shortcuts, music playback,
Wikipedia search, time/date, weather, news, app launching, ChatGPT
integration, system controls, screenshots, volume control, and file search.

SETUP NOTES:
- Install dependencies:
    pip install SpeechRecognition pyttsx3 pyaudio wikipedia-api requests
    pip install pyautogui pycaw comtypes opencv-python  # optional features
- Set NEWS_API_KEY and GEMINI_API_KEY as environment variables (see below).
- Volume control (pycaw) and some app paths are Windows-specific.
  Adjust APP_PATHS and the volume section for macOS/Linux if needed.
"""

import speech_recognition as sr
import pyttsx3
import webbrowser
import wikipediaapi
import requests
import datetime
import subprocess
import os
import sys
import platform
import difflib

# -----------------------------
# Config — set these as environment variables, don't hardcode keys here
#   Windows (Powershell):  setx NEWS_API_KEY "your_key"
#   macOS/Linux (bash):    export NEWS_API_KEY="your_key"
# Then restart your terminal so the variable is picked up.
# -----------------------------
NEWS_API_KEY = os.environ.get("NEWS_API_KEY", "")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")

# -----------------------------
# Initialize
# -----------------------------
recognizer = sr.Recognizer()

wiki = wikipediaapi.Wikipedia(
    language="en",
    user_agent="JarvisAssistant/1.0"
)

# -----------------------------
# Text to Speech
# A fresh engine is created on every call — reusing one global engine object
# is a known cause of pyttsx3 silently going quiet after a few calls on Windows.
# -----------------------------
def speak(text):
    print("Jarvis:", text)
    try:
        engine = pyttsx3.init()
        engine.setProperty("rate", 175)
        engine.say(text)
        engine.runAndWait()
        engine.stop()
    except Exception as e:
        print("Speak Error:", e)

# -----------------------------
# Music Library
# -----------------------------
music = {
    "stealth": "https://www.youtube.com/watch?v=U47Tr9BB_wE",
    "faded": "https://www.youtube.com/watch?v=60ItHLzjLm4",
    "tere sang": "https://www.youtube.com/watch?v=nNIWzcnifd4",
    "raatein": "https://www.youtube.com/watch?v=nNIWzcnifd4",
    "tum hi ho": "https://www.youtube.com/watch?v=Umqb9KENgmk",
}

# -----------------------------
# Websites (add more anytime — key = spoken word, value = URL)
# -----------------------------
WEBSITES = {
    "google": "https://www.google.com",
    "youtube": "https://www.youtube.com",
    "github": "https://github.com",
    "telegram": "https://web.telegram.org",
    "chatgpt": "https://chat.openai.com",
    "instagram": "https://www.instagram.com",
    "facebook": "https://www.facebook.com",
    "whatsapp web": "https://web.whatsapp.com",
    "twitter": "https://twitter.com",
    "linkedin": "https://www.linkedin.com",
    "reddit": "https://www.reddit.com",
    "netflix": "https://www.netflix.com",
    "amazon": "https://www.amazon.in",
    "gmail": "https://mail.google.com",
    "maps": "https://maps.google.com",
    "spotify web": "https://open.spotify.com",
    "cloud": "https://claude.ai",
    "poki games": "https://poki.com",
}

# -----------------------------
# Windows apps (key = spoken word, value = launch command)
# Uses "start <value>" so both .exe names and protocol handlers work.
# NOTE: Windows-only. Adjust for macOS/Linux if needed.
# -----------------------------
WINDOWS_APPS = {
    "notepad": "notepad",
    "calculator": "calc",
    "paint": "mspaint",
    "wordpad": "write",
    "camera": "microsoft.windows.camera:",
    "photos": "ms-photos:",
    "settings": "ms-settings:",
    "control panel": "control",
    "task manager": "taskmgr",
    "file explorer": "explorer",
    "command prompt": "cmd",
    "powershell": "powershell",
    "snipping tool": "ms-screenclip:",
    "media player": "wmplayer",
    "edge": "msedge",
    "chrome": "chrome",
    "vs code": "code",
    "visual studio code": "code",
    "word": "winword",
    "excel": "excel",
    "powerpoint": "powerpnt",
    "outlook": "outlook",
    "spotify": "spotify",
    "whatsapp": "whatsapp:",
}

# -----------------------------
# Apps that can be closed by name (key = spoken word, value = Windows process name)
# -----------------------------
CLOSE_APPS = {
    "notepad": "notepad.exe",
    "calculator": "CalculatorApp.exe",
    "paint": "mspaint.exe",
    "wordpad": "wordpad.exe",
    "camera": "WindowsCamera.exe",
    "task manager": "Taskmgr.exe",
    "media player": "wmplayer.exe",
    "edge": "msedge.exe",
    "chrome": "chrome.exe",
    "vs code": "Code.exe",
    "word": "WINWORD.EXE",
    "excel": "EXCEL.EXE",
    "powerpoint": "POWERPNT.EXE",
    "outlook": "OUTLOOK.EXE",
    "spotify": "Spotify.exe",
}

# -----------------------------
# Custom apps/folders specific to YOUR laptop.
# EDIT THESE PATHS to match where things actually are on your system.
# Right-click the app's shortcut -> Properties -> copy the "Target" path.
# For folders, just paste the folder path.
# -----------------------------
CUSTOM_APPS = {
    "ai voice": r"e:\ai voice",  # your project folder — already correct
    "pokimmo": r"D:\PS3\PokeMMO\PokeMMO.exe",
}

# -----------------------------
# Helper: Weather (Open-Meteo, no API key needed)
# -----------------------------
def get_weather(city):
    try:
        geo = requests.get(
            "https://geocoding-api.open-meteo.com/v1/search",
            params={"name": city, "count": 1},
            timeout=10,
        ).json()
        if "results" not in geo:
            return None
        lat = geo["results"][0]["latitude"]
        lon = geo["results"][0]["longitude"]
        resolved_name = geo["results"][0]["name"]

        weather = requests.get(
            "https://api.open-meteo.com/v1/forecast",
            params={"latitude": lat, "longitude": lon, "current_weather": True},
            timeout=10,
        ).json()
        temp = weather["current_weather"]["temperature"]
        wind = weather["current_weather"]["windspeed"]
        return f"The current temperature in {resolved_name} is {temp} degrees Celsius, with wind speed {wind} kilometers per hour."
    except Exception:
        return None

# -----------------------------
# Helper: News (NewsAPI)
# -----------------------------
def get_news(query=None):
    try:
        if query:
            url = "https://newsapi.org/v2/everything"
            params = {
                "q": query,
                "apiKey": NEWS_API_KEY,
                "pageSize": 5,
                "sortBy": "publishedAt",
                "language": "en",
            }
        else:
            url = "https://newsapi.org/v2/top-headlines"
            params = {"country": "in", "apiKey": NEWS_API_KEY, "pageSize": 5}

        response = requests.get(url, params=params, timeout=10).json()
        articles = response.get("articles", [])

        if not articles:
            # Fallback: no articles found — ask the AI so the user still gets an answer
            if query:
                return ask_ai(f"Give me a brief, current summary of news or recent developments about {query}.")
            return "I couldn't fetch any news right now."

        headlines = [a["title"] for a in articles]
        prefix = f"Here are the latest headlines about {query}." if query else "Here are the top headlines."
        return prefix + " " + ". ".join(headlines)
    except Exception:
        # Fallback: NewsAPI request itself failed — still try to answer via AI
        if query:
            return ask_ai(f"Give me a brief, current summary of news or recent developments about {query}.")
        return "Something went wrong while fetching the news."

# -----------------------------
# Helper: AI chat (Gemini, free tier)
# -----------------------------
def ask_ai(query):
    if not GEMINI_API_KEY:
        return "I don't have a Gemini API key set. Please set the GEMINI_API_KEY environment variable."
    try:
        url = (
            "https://generativelanguage.googleapis.com/v1beta/models/"
            f"gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"
        )
        payload = {"contents": [{"parts": [{"text": query}]}]}
        response = requests.post(url, json=payload, timeout=15).json()
        return response["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e:
        return f"I couldn't reach the AI service. Error: {e}"

# -----------------------------
# Helper: Screenshot
# -----------------------------
def take_screenshot():
    try:
        import pyautogui
        folder = os.path.join(os.path.expanduser("~"), "Pictures")
        os.makedirs(folder, exist_ok=True)
        filename = os.path.join(
            folder, f"screenshot_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        )
        img = pyautogui.screenshot()
        img.save(filename)
        return filename
    except Exception:
        return None

# -----------------------------
# Helper: Volume control (Windows only, via pycaw)
# -----------------------------
def set_volume(action):
    if platform.system() != "Windows":
        print("Volume Error: Not on Windows, volume control unsupported.")
        return False
    try:
        from ctypes import cast, POINTER
        from comtypes import CLSCTX_ALL
        from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

        devices = AudioUtilities.GetSpeakers()
        try:
            interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        except AttributeError:
            # Newer pycaw versions wrap the raw COM device inside devices._dev
            interface = devices._dev.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        current = volume.GetMasterVolumeLevelScalar()

        if action == "up":
            volume.SetMasterVolumeLevelScalar(min(current + 0.1, 1.0), None)
        elif action == "down":
            volume.SetMasterVolumeLevelScalar(max(current - 0.1, 0.0), None)
        elif action == "mute":
            volume.SetMute(1, None)
        elif action == "unmute":
            volume.SetMute(0, None)
        return True
    except Exception as e:
        print("Volume Error:", e)
        return False

# -----------------------------
# Helper: Take a photo using the webcam
# -----------------------------
def capture_photo():
    try:
        import cv2
        backend = cv2.CAP_DSHOW if platform.system() == "Windows" else cv2.CAP_ANY
        cam = cv2.VideoCapture(0, backend)
        if not cam.isOpened():
            print("Camera Error: Could not open webcam (index 0). Is it in use by another app like Windows Camera?")
            return None
        ret, frame = cam.read()
        cam.release()
        if not ret:
            print("Camera Error: Failed to read frame from webcam. Close any other app using the camera (e.g. Windows Camera app) and try again.")
            return None
        folder = os.path.join(os.path.expanduser("~"), "Pictures")
        os.makedirs(folder, exist_ok=True)
        filename = os.path.join(
            folder, f"photo_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
        )
        cv2.imwrite(filename, frame)
        return filename
    except Exception as e:
        print("Camera Error:", e)
        return None

# -----------------------------
# Helper: Record a short video using the webcam
# -----------------------------
def record_video(duration=5):
    try:
        import cv2
        import time
        backend = cv2.CAP_DSHOW if platform.system() == "Windows" else cv2.CAP_ANY
        cam = cv2.VideoCapture(0, backend)
        if not cam.isOpened():
            print("Camera Error: Could not open webcam (index 0). Is it in use by another app like Windows Camera?")
            return None
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        folder = os.path.join(os.path.expanduser("~"), "Videos")
        os.makedirs(folder, exist_ok=True)
        filename = os.path.join(
            folder, f"video_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4"
        )
        frame_width = int(cam.get(3))
        frame_height = int(cam.get(4))
        out = cv2.VideoWriter(filename, fourcc, 20.0, (frame_width, frame_height))

        start = time.time()
        while time.time() - start < duration:
            ret, frame = cam.read()
            if not ret:
                print("Camera Error: Failed to read frame during recording.")
                break
            out.write(frame)

        cam.release()
        out.release()
        return filename
    except Exception as e:
        print("Camera Error:", e)
        return None

# -----------------------------
# Helper: Open a custom app or folder (from CUSTOM_APPS)
# -----------------------------
def open_custom_app(path):
    try:
        if os.path.isdir(path):
            os.startfile(path)
        elif os.path.isfile(path):
            subprocess.Popen(path, shell=True)
        else:
            print(f"Custom App Error: Path does not exist -> {path}")
            return False
        return True
    except Exception as e:
        print("Custom App Error:", e)
        return False

# -----------------------------
# Helper: Get the top YouTube video for a search query (opens video directly, not just search page)
# -----------------------------
def get_top_youtube_video(query):
    try:
        import re
        from urllib.parse import quote
        search_url = f"https://www.youtube.com/results?search_query={quote(query)}"
        html = requests.get(search_url, timeout=10).text
        video_ids = re.findall(r"watch\?v=(\S{11})", html)
        if video_ids:
            return f"https://www.youtube.com/watch?v={video_ids[0]}"
        return None
    except Exception as e:
        print("YouTube Search Error:", e)
        return None

# -----------------------------
# Helper: File search
# -----------------------------
def search_file(filename, search_root=None):
    if search_root is None:
        search_root = os.path.expanduser("~")
    matches = []
    for root, dirs, files in os.walk(search_root):
        for f in files:
            if filename.lower() in f.lower():
                matches.append(os.path.join(root, f))
                if len(matches) >= 5:
                    return matches
    return matches

# -----------------------------
# Process Commands
# -----------------------------
def processCommand(command):
    command = command.lower()

    # Handle "close" FIRST, before any open-website/app matching.
    # (Otherwise "close chrome" would match the word "chrome" in the open-app logic below and open it instead.)
    if "close" in command:
        target = command.replace("close", "").strip()
        if target == "" or "window" in target or "this" in target:
            try:
                import pyautogui
                pyautogui.hotkey("alt", "f4")
                speak("Closing the active window")
            except Exception as e:
                print("Close Window Error:", e)
                speak("I couldn't close the window.")
        else:
            closed = False
            for name in sorted(CLOSE_APPS.keys(), key=len, reverse=True):
                if name in target:
                    if platform.system() == "Windows":
                        os.system(f"taskkill /IM {CLOSE_APPS[name]} /F")
                        speak(f"Closing {name}")
                    else:
                        speak("Closing apps isn't supported on this system yet.")
                    closed = True
                    break
            if not closed:
                speak(f"I don't know how to close {target}. Try saying 'close window' to close the active one.")
        return

    # Open Websites (checked first, longer/more specific keys checked before generic ones)
    matched = False
    for site_name in sorted(WEBSITES.keys(), key=len, reverse=True):
        if site_name in command:
            speak(f"Opening {site_name}")
            webbrowser.open(WEBSITES[site_name])
            matched = True
            break

    # Open Windows apps
    if not matched:
        for app_name in sorted(WINDOWS_APPS.keys(), key=len, reverse=True):
            if app_name in command:
                speak(f"Opening {app_name}")
                if platform.system() == "Windows":
                    os.system(f"start {WINDOWS_APPS[app_name]}")
                else:
                    speak(f"{app_name} isn't supported on this system yet.")
                matched = True
                break

    # Open custom apps/folders (edit CUSTOM_APPS dict with your real paths)
    if not matched:
        for custom_name in sorted(CUSTOM_APPS.keys(), key=len, reverse=True):
            if custom_name in command:
                speak(f"Opening {custom_name}")
                if not open_custom_app(CUSTOM_APPS[custom_name]):
                    speak(f"I couldn't find {custom_name}. Please check the path in the script.")
                matched = True
                break

    if matched:
        pass

    # Play Music (any song — checks the fixed list first, then falls back to YouTube search)
    elif "play" in command:
        song = command.replace("play music", "").replace("play", "").strip()
        if song == "":
            speak("Please tell me the song name.")
        elif song in music:
            speak(f"Playing {song}")
            webbrowser.open(music[song])
        else:
            close = difflib.get_close_matches(song, music.keys(), n=1, cutoff=0.5)
            if close:
                speak(f"Playing {close[0]}")
                webbrowser.open(music[close[0]])
            else:
                speak(f"Searching YouTube for {song}")
                top_video = get_top_youtube_video(song)
                if top_video:
                    webbrowser.open(top_video)
                else:
                    from urllib.parse import quote
                    webbrowser.open(f"https://www.youtube.com/results?search_query={quote(song)}")

    # Wikipedia Search
    elif "who is" in command or "what is" in command and "time" not in command and "date" not in command:
        topic = command.replace("who is", "").replace("what is", "").strip()
        speak(f"Searching Wikipedia for {topic}")
        page = wiki.page(topic)
        if page.exists():
            summary = page.summary.split(". ")
            short_summary = ". ".join(summary[:2])
            print(short_summary)
            speak(short_summary)
        else:
            speak("Sorry, I couldn't find that on Wikipedia.")

    # Time & Date
    elif "time" in command:
        now = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The current time is {now}")
    elif "date" in command:
        today = datetime.datetime.now().strftime("%B %d, %Y")
        speak(f"Today's date is {today}")

    # Weather
    elif "weather" in command:
        city = command.replace("weather in", "").replace("weather", "").strip()
        if not city:
            speak("Please tell me which city.")
        else:
            result = get_weather(city)
            speak(result if result else f"Sorry, I couldn't find weather for {city}.")

    # News (general or topic/region specific, e.g. "punjab news", "news about cricket")
    elif "news" in command:
        topic = command.replace("news", "").replace("about", "").strip()
        speak(f"Fetching the latest headlines about {topic}" if topic else "Fetching the latest headlines")
        speak(get_news(topic if topic else None))

    # AI chat (Gemini)
    elif "ask jarvis" in command or "ask gpt" in command or "ask gemini" in command:
        query = command.replace("ask jarvis", "").replace("ask gpt", "").replace("ask gemini", "").strip()
        if not query:
            speak("What would you like to ask?")
        else:
            speak("Let me think")
            speak(ask_ai(query))

    # Screenshot
    elif "take a screenshot" in command or "screenshot" in command:
        path = take_screenshot()
        speak(f"Screenshot saved to {path}" if path else "Sorry, I couldn't take a screenshot.")

    # Take a photo (webcam)
    elif "take a photo" in command or "take photo" in command or "click photo" in command or "click a photo" in command:
        speak("Say cheese")
        path = capture_photo()
        speak(f"Photo saved to {path}" if path else "Sorry, I couldn't access the camera.")

    # Record a video (webcam, 5 seconds)
    elif "make video" in command or "make a video" in command or "record video" in command or "record a video" in command:
        speak("Recording a 5 second video")
        path = record_video(5)
        speak(f"Video saved to {path}" if path else "Sorry, I couldn't access the camera.")

    # Open a file by name anywhere on the system
    elif "open file" in command:
        filename = command.replace("open file", "").strip()
        if not filename:
            speak("Which file should I open?")
        else:
            speak(f"Searching for {filename}")
            results = search_file(filename)
            if results:
                speak(f"Opening {results[0]}")
                os.startfile(results[0])
            else:
                speak("I couldn't find that file.")

    # Close an app by name, or the currently active window
    # Volume control
    elif "volume up" in command or "increase volume" in command or "turn up the volume" in command:
        speak("Increasing volume") if set_volume("up") else speak("Volume control isn't working — check the terminal for the error.")
    elif "volume down" in command or "decrease volume" in command or "turn down the volume" in command:
        speak("Decreasing volume") if set_volume("down") else speak("Volume control isn't working — check the terminal for the error.")
    elif "unmute" in command:
        speak("Unmuting") if set_volume("unmute") else speak("Volume control isn't working — check the terminal for the error.")
    elif "mute" in command:
        speak("Muting") if set_volume("mute") else speak("Volume control isn't working — check the terminal for the error.")

    # File search
    elif "find file" in command or "search file" in command:
        filename = command.replace("find file", "").replace("search file", "").strip()
        if not filename:
            speak("What file should I search for?")
        else:
            speak(f"Searching for {filename}")
            results = search_file(filename)
            if results:
                speak(f"I found {len(results)} matching files. The first one is {results[0]}")
                print("\n".join(results))
            else:
                speak("I couldn't find that file.")

    # Shutdown / Restart (use with caution)
    elif "shutdown" in command:
        speak("Shutting down the system in 10 seconds. Say cancel shutdown to stop.")
        if platform.system() == "Windows":
            os.system("shutdown /s /t 10")
        else:
            os.system("shutdown -h +0.1")
    elif "restart" in command:
        speak("Restarting the system in 10 seconds.")
        if platform.system() == "Windows":
            os.system("shutdown /r /t 10")
        else:
            os.system("shutdown -r +0.1")
    elif "cancel shutdown" in command:
        if platform.system() == "Windows":
            os.system("shutdown /a")
        speak("Shutdown cancelled.")

    # Exit
    elif "exit" in command or "stop jarvis" in command:
        speak("Goodbye Sir.")
        sys.exit()

    # Unknown command
    else:
        speak("Sorry, I did not understand that command.")

# -----------------------------
# Main Program
# -----------------------------
if __name__ == "__main__":
    speak("Initializing Jarvis")

    # Step 1: Wait for wake word ONCE
    while True:
        try:
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source, duration=1)
                print("\nSay 'Jarvis' to activate...")
                audio = recognizer.listen(source, timeout=10, phrase_time_limit=5)

            wake_word = recognizer.recognize_google(audio).lower()
            print("You said:", wake_word)

            if "jarvis" in wake_word:
                speak("Jarvis is ready. I am listening for your commands.")
                break

        except sr.WaitTimeoutError:
            print("No speech detected.")
        except sr.UnknownValueError:
            print("Sorry, I couldn't understand.")
        except sr.RequestError:
            print("Internet connection required for speech recognition.")
        except Exception as e:
            print("Error:", e)

    # Step 2: Keep listening for commands directly, no wake word needed anymore
    is_paused = False
    while True:
        try:
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source, duration=1)
                print("\nListening for command..." if not is_paused else "\n[Paused] Listening for 'start' to resume...")
                audio = recognizer.listen(source, timeout=10, phrase_time_limit=8)

            command = recognizer.recognize_google(audio)
            command_lower = command.lower().strip()
            print("Command:", command)

            # Hard exit
            if "exit" in command_lower or "stop jarvis" in command_lower or "shutdown jarvis" in command_lower:
                speak("Goodbye Sir.")
                sys.exit()

            # Pause listening (does not exit the program)
            elif command_lower in ("stop", "pause") or "stop listening" in command_lower or "pause listening" in command_lower:
                is_paused = True
                speak("Paused. Say start whenever you need me.")

            # Resume listening
            elif command_lower in ("start", "resume") or "start listening" in command_lower or "resume listening" in command_lower:
                is_paused = False
                speak("Yes Sir, I am listening again.")

            # While paused, ignore everything else
            elif is_paused:
                print("Currently paused — ignoring command. Say 'start' to resume.")

            # Normal command processing
            else:
                speak("Yes Sir")
                processCommand(command)

        except sr.WaitTimeoutError:
            print("No speech detected.")
        except sr.UnknownValueError:
            print("Sorry, I couldn't understand.")
        except sr.RequestError:
            print("Internet connection required for speech recognition.")
        except SystemExit:
            break
        except Exception as e:
            print("Error:", e)