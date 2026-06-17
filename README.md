SkyBot – AI Voice Weather Assistant 🌤️🎤
Overview

SkyBot is an AI-powered Voice Weather Assistant that provides real-time weather updates and rainfall predictions through both text and voice interactions. The application integrates speech recognition, text-to-speech, and weather APIs to deliver a seamless hands-free user experience.

Features
🌦️ Real-time weather updates for any city
🎤 Voice-based weather queries using Speech Recognition
🔊 Text-to-Speech responses using gTTS
☔ Rainfall prediction and alerts
📅 3-Day weather forecast
🌍 City-wise weather tracking
📊 Interactive and responsive web dashboard
🔄 REST API backend built with Flask
Technologies Used
Python
Flask
HTML, CSS, JavaScript
OpenWeatherMap API
SpeechRecognition
gTTS (Google Text-to-Speech)
Pygame
Flask-CORS
Project Architecture
User Voice/Input
        │
        ▼
Speech Recognition
        │
        ▼
Flask Backend API
        │
        ▼
OpenWeatherMap API
        │
        ▼
Weather & Forecast Data
        │
        ▼
Text-to-Speech + Dashboard Output
Installation
Clone the Repository
git clone https://github.com/bhargavi1608/SkyBot-Weather-Prediction.git
cd SkyBot-Weather-Prediction
Install Dependencies
pip install flask flask-cors requests gtts pygame SpeechRecognition
Running the Application
Start Backend
python main.py

Backend runs on:

http://127.0.0.1:5000
Open Frontend

Open index.html in your browser.

API Endpoints
Get Current Weather
GET /weather?city=Mumbai
Check Rain Prediction
GET /rain?city=Delhi
Voice Query
GET /voice
Example Voice Commands
Weather in Hyderabad
What's the temperature in Mumbai?
Will it rain in Delhi today?
Weather in Bangalore



Future Enhancements
🤖 AI chatbot integration with LLMs
📍 GPS-based weather detection
🌐 Multi-language support
📱 Mobile application deployment
📈 Advanced weather analytics dashboard
🔔 Real-time severe weather notifications
Learning Outcomes
REST API Development with Flask
API Integration and Data Processing
Speech Recognition Systems
Text-to-Speech Applications
Frontend-Backend Communication
Real-Time Weather Data Analysis
Author

Pulloju Bhargavi

B.Tech CSE | AI & Machine Learning Enthusiast

GitHub: https://github.com/bhargavi1608
