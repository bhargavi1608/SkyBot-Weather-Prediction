# 🌤️ SkyBot – AI Voice Weather Assistant 🎤

## 📌 Overview

SkyBot is an AI-powered Voice Weather Assistant that provides real-time weather updates and rainfall predictions through both text and voice interactions. The application integrates Speech Recognition, Text-to-Speech (TTS), and Weather APIs to deliver a seamless hands-free user experience. Users can check weather conditions, forecast information, and rainfall alerts simply by speaking or entering a city name.

---

## ✨ Features

- 🌦️ Real-time weather updates for any city
- 🎤 Voice-based weather queries using Speech Recognition
- 🔊 Text-to-Speech responses using Google Text-to-Speech (gTTS)
- ☔ Rainfall prediction and weather alerts
- 📅 3-Day weather forecast
- 🌍 City-wise weather tracking
- 📊 Interactive and responsive web dashboard
- 🔄 REST API backend built with Flask

---

## 🛠️ Technologies Used

### Backend
- Python
- Flask
- Flask-CORS

### Frontend
- HTML
- CSS
- JavaScript

### APIs & Libraries
- OpenWeatherMap API
- SpeechRecognition
- gTTS (Google Text-to-Speech)
- Pygame
- Requests

---

## 🏗️ Project Architecture

```text
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
```

---

## 🚀 Installation

### Clone the Repository

```bash
git clone https://github.com/bhargavi1608/SkyBot-Weather-Prediction.git
cd SkyBot-Weather-Prediction
```

### Install Dependencies

```bash
pip install flask flask-cors requests gtts pygame SpeechRecognition
```

---

## ▶️ Running the Application

### Start the Backend Server

```bash
python main.py
```

Backend will run at:

```text
http://127.0.0.1:5000
```

### Launch the Frontend

Open the `index.html` file in your browser.

---

## 🔗 API Endpoints

### Get Current Weather

```http
GET /weather?city=Mumbai
```

### Check Rain Prediction

```http
GET /rain?city=Delhi
```

### Voice Query

```http
GET /voice
```

---

## 🎙️ Example Voice Commands

```text
Weather in Hyderabad
What's the temperature in Mumbai?
Will it rain in Delhi today?
Weather in Bangalore
```

---

## 🎯 Learning Outcomes

- REST API Development using Flask
- API Integration and Data Processing
- Speech Recognition Systems
- Text-to-Speech Applications
- Frontend–Backend Communication
- Real-Time Weather Data Analysis
- Building Interactive AI-Based Applications

---

## 🔮 Future Enhancements

- 🤖 AI chatbot integration using Large Language Models (LLMs)
- 📍 GPS-based weather detection
- 🌐 Multi-language support
- 📱 Mobile application deployment
- 📈 Advanced weather analytics dashboard
- 🔔 Real-time severe weather notifications
- ☁️ Cloud deployment for global accessibility

---

## 👩‍💻 Author

**Pulloju Bhargavi**  
B.Tech – Computer Science Engineering  
AI & Machine Learning Enthusiast

GitHub: https://github.com/bhargavi1608

---

⭐ If you found this project useful, consider giving it a star on GitHub!
