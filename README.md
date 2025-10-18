
# SmartForm AI

## Overview
SmartForm AI is a real-time workout form analyzer that supports multiple exercises (Pushups, Squats, Lunges). It uses pose estimation and ML models to classify rep quality and GPT to generate human-readable feedback.

## Features
- Multi-exercise support with dynamic guidance
- Real-time form classification (Good / Needs Improvement / Bad)
- Human-friendly feedback using GPT
- Optional skeleton overlay with angle highlights

## Tech Stack
- **MediaPipe**: Pose landmark extraction
- **Python / Scikit-learn / XGBoost**: ML classifiers
- **GPT (OpenAI API or local LLM)**: Text guidance
- **FastAPI**: Backend API
- **HTML / JS / CSS**: Frontend interface

## Setup Instructions
1. Clone the repository
2. Install dependencies:
```bash
pip install mediapipe scikit-learn xgboost fastapi uvicorn
