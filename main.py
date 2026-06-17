"""
SkyBot Backend — skybot_backend.py
===================================
Serves weather data as a REST API for index.html
Also runs the original voice loop (mic → gTTS → pygame) if you prefer terminal mode.

Requirements:
    pip install flask flask-cors requests gtts pygame SpeechRecognition

Run:
    python skybot_backend.py

Endpoints:
    GET /weather?city=Mumbai   → current weather JSON
    GET /rain?city=Mumbai      → rain prediction JSON
    GET /voice                 → starts one voice query cycle (terminal mode)
"""

import os
import uuid
import time
import threading

import requests
import speech_recognition as sr
from gtts import gTTS
import pygame
from flask import Flask, request, jsonify
from flask_cors import CORS

# ── Config ────────────────────────────────────────────────────────────────────

API_KEY      = "Your_API"   # OpenWeatherMap API key
DEFAULT_CITY = "Hyderabad,IN"
HOST         = "127.0.0.1"
PORT         = 5000

# ── Flask app ─────────────────────────────────────────────────────────────────

app = Flask(__name__)
CORS(app)   # allow requests from the HTML file opened locally

pygame.mixer.init()

# ── TTS (gTTS + pygame) ───────────────────────────────────────────────────────

def speak(text: str) -> None:
    """Convert text to speech and play it."""
    print(f"[Bot] {text}")
    try:
        filename = f"voice_{uuid.uuid4().hex}.mp3"
        tts = gTTS(text=text, lang="en")
        tts.save(filename)

        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            time.sleep(0.1)

        pygame.mixer.music.stop()
        pygame.mixer.music.unload()
        time.sleep(0.3)
        os.remove(filename)

    except Exception as e:
        print(f"[TTS Error] {e}")


# ── Microphone ────────────────────────────────────────────────────────────────

def listen() -> str:
    """Capture one voice command and return it as lowercase text."""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("[Mic] Listening...")
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=8)
            text  = r.recognize_google(audio)
            print(f"[You] {text}")
            return text.lower()
        except sr.WaitTimeoutError:
            return ""
        except sr.UnknownValueError:
            return ""
        except Exception as e:
            print(f"[Mic Error] {e}")
            return ""


# ── City parser ───────────────────────────────────────────────────────────────

def extract_city(query: str, default: str = DEFAULT_CITY) -> str:
    """
    Pull the city name from a natural-language query.
    'weather in new york today' → 'new york,IN'
    """
    STOP_WORDS = {"today", "now", "tomorrow", "please", "the", "a", "an"}

    if " in " in query:
        after = query.split(" in ", 1)[1]
        words = [
            w.strip("?.,!")
            for w in after.split()
            if w.strip("?.,!").lower() not in STOP_WORDS
        ]
        if words:
            return " ".join(words).title() + ",IN"

    return default


# ── Weather helpers ───────────────────────────────────────────────────────────

def get_weather(city: str) -> dict:
    """
    Fetch current weather from OpenWeatherMap.
    Returns a dict ready to send as JSON to the frontend.
    """
    url = (
        f"http://api.openweathermap.org/data/2.5/weather"
        f"?q={city}&appid={API_KEY}&units=metric"
    )
    resp = requests.get(url, timeout=8)
    data = resp.json()

    if resp.status_code != 200:
        return {"error": f"City not found: {city}"}

    return {
        "city":        data["name"],
        "temp":        round(data["main"]["temp"]),
        "feels_like":  round(data["main"]["feels_like"]),
        "humidity":    data["main"]["humidity"],
        "wind_kmh":    round(data["wind"].get("speed", 0) * 3.6),
        "description": data["weather"][0]["description"],
    }


def get_forecast(city: str) -> list:
    """
    Fetch 3-day (24 x 3-hour slots = 72 h) forecast.
    Returns a list of {temp, description} dicts.
    """
    url = (
        f"http://api.openweathermap.org/data/2.5/forecast"
        f"?q={city}&appid={API_KEY}&units=metric&cnt=24"
    )
    resp = requests.get(url, timeout=8)
    data = resp.json()

    if resp.status_code != 200 or "list" not in data:
        return []

    return [
        {
            "temp":        round(item["main"]["temp"]),
            "description": item["weather"][0]["description"],
        }
        for item in data["list"]
    ]


def check_rain(city: str) -> dict:
    """
    Look at next 24 hours of forecast; return rain prediction.
    """
    url = (
        f"http://api.openweathermap.org/data/2.5/forecast"
        f"?q={city}&appid={API_KEY}&units=metric&cnt=8"
    )
    resp = requests.get(url, timeout=8)
    data = resp.json()

    if resp.status_code != 200 or "list" not in data:
        return {"error": f"Could not check rainfall for {city}", "rain": False}

    has_rain = any(
        "rain" in item["weather"][0]["description"].lower()
        for item in data["list"]
    )

    message = (
        f"Rain expected in {city} in the next few hours — carry an umbrella."
        if has_rain else
        f"No rain expected in {city} today."
    )
    return {"city": city, "rain": has_rain, "message": message}


# ── Flask routes ──────────────────────────────────────────────────────────────

@app.route("/weather")
def route_weather():
    city = request.args.get("city", DEFAULT_CITY)
    result = get_weather(city)
    if "error" not in result:
        result["forecast"] = get_forecast(city)
    return jsonify(result)


@app.route("/rain")
def route_rain():
    city = request.args.get("city", DEFAULT_CITY)
    return jsonify(check_rain(city))


@app.route("/voice")
def route_voice():
    """
    Trigger one voice-listen cycle from the browser (optional).
    The result is returned as JSON; the frontend can display it.
    """
    query = listen()
    if not query:
        return jsonify({"heard": "", "response": "I didn't catch that."})

    city = extract_city(query)

    if "weather" in query or "temperature" in query:
        weather = get_weather(city)
        if "error" in weather:
            msg = weather["error"]
        else:
            msg = (
                f"The weather in {weather['city']} is {weather['description']}. "
                f"Temperature {weather['temp']} degrees, "
                f"feels like {weather['feels_like']}, "
                f"humidity {weather['humidity']} percent."
            )
        speak(msg)
        return jsonify({"heard": query, "response": msg})

    elif "rain" in query:
        result = check_rain(city)
        msg    = result.get("message", "Unable to check rain.")
        speak(msg)
        return jsonify({"heard": query, "response": msg})

    else:
        msg = "Please ask about weather or rain in a city."
        speak(msg)
        return jsonify({"heard": query, "response": msg})


@app.route("/")
def root():
    return jsonify({
        "status":    "SkyBot backend running",
        "endpoints": ["/weather?city=Mumbai", "/rain?city=Delhi", "/voice"]
    })


# ── Terminal voice loop (optional) ────────────────────────────────────────────

def terminal_voice_loop():
    """
    Runs the original voice bot loop in the terminal.
    Called only if you want the mic-based loop alongside the API.
    """
    speak("SkyBot started. Ask me about weather or rain.")
    while True:
        query = listen()
        if not query:
            continue

        city = extract_city(query)

        if "weather" in query or "temperature" in query:
            data = get_weather(city)
            if "error" in data:
                speak(data["error"])
            else:
                speak(
                    f"The weather in {data['city']} is {data['description']}. "
                    f"Temperature is {data['temp']} degrees Celsius, "
                    f"feels like {data['feels_like']}, "
                    f"humidity {data['humidity']} percent."
                )

        elif "rain" in query:
            result = check_rain(city)
            speak(result.get("message", "Unable to check rain."))

        elif "exit" in query or "stop" in query:
            speak("Goodbye!")
            break

        else:
            speak("Try asking: weather in Delhi, or rain in Mumbai.")


# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="SkyBot backend")
    parser.add_argument(
        "--voice-loop",
        action="store_true",
        help="Also run the terminal voice loop alongside the API server"
    )
    args = parser.parse_args()

    if args.voice_loop:
        # Run voice loop in a background thread, API server in main thread
        t = threading.Thread(target=terminal_voice_loop, daemon=True)
        t.start()

    print(f"\n🌤  SkyBot backend running at http://{HOST}:{PORT}")
    print(f"    Open skybot_frontend.html in Chrome to use the UI\n")

    app.run(host=HOST, port=PORT, debug=False)