# Reaction Time Proxy API

## 📌 Overview
This API estimates a fielder's reaction performance using indirect match-event data.

## 🚀 Setup

pip install -r requirements.txt  
uvicorn main:app --reload  

## 📍 Endpoint
POST /predict/reaction

## 📥 Sample Request
{
  "ball_speed": 22,
  "distance": 12,
  "event_time": 1.8,
  "movement_start_delay": 0.4,
  "outcome": 1
}

## 📤 Sample Response
{
  "reaction_score": 0.78,
  "pressure_index": 42.3,
  "verdict": "Good"
}

## 📊 Interpretation
- Higher score → better reaction
- Pressure index → how tight the timing was