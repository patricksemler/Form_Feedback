# Form Feedback

## Description

**Form Feedback** is an AI-driven fitness app that helps users analyze their exercise form through video feedback. Users can upload videos of exercises (e.g., push-ups, sit-ups, squats, lunges), and the system provides real-time feedback on their form. The app uses computer vision to detect joint angles and movements, and AI (powered by GPT) is utilized to generate detailed reports, summaries, and personalized feedback on users' performance.

The project is composed of two main components:

1. **Backend** - A FastAPI server that processes uploaded exercise videos, analyzes them for joint angles and posture, and integrates GPT to generate feedback reports.
2. **Frontend** - A React Native mobile app that allows users to upload videos, select exercises, and view feedback summaries and suggestions.

## Tech Stack

* **Backend**:

  * FastAPI (Python)
  * OpenCV & cvzone (for pose detection and video processing)
  * Uvicorn (ASGI server)
  * GPT (for generating feedback reports and exercise summaries)
  * Pose Detection Model (for joint angle calculations)

* **Frontend**:

  * React Native
  * Expo (for image and video picking)
  * Expo Router (for navigation)

* **Machine Learning / Pose Detection**:

  * OpenCV
  * MediaPipe Pose (via cvzone)
  * GPT (for generating personalized feedback and summaries)

## Setup Instructions

### Backend (Python)

1. Clone this repository:

   ```bash
   git clone https://github.com/patricksemler/Form_Feedback.git
   cd Form_Feedback/backend
   ```

2. Set up a Python virtual environment:

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows, use venv\Scripts\activate
   ```

3. Install the required dependencies:

   ```bash
   pip install fastapi uvicorn opencv-python cvzone numpy openai
   ```

4. Start the FastAPI server:

   ```bash
   uvicorn app:app --host 0.0.0.0 --port 5001 --reload
   ```

   The backend will run on `http://localhost:5001`.

### Frontend (React Native with Expo)

1. Clone this repository:

   ```bash
   git clone https://github.com/patricksemler/Form_Feedback.git
   cd Form_Feedback/frontend
   ```

2. Install Expo CLI (if not already installed):

   ```bash
   npm install -g expo-cli
   ```

3. Install the required dependencies:

   ```bash
   npm install
   ```

4. Start the Expo development server:

   ```bash
   npm start
   ```

5. Open the app on your mobile device or emulator to start using the Form Feedback app.

### Configuration

* **Server IP**: The React Native app uses `http://localhost:5001` for the backend.
* **Exercise Options**: The app supports multiple exercises (Push-Up, Sit-Up, Squat, Lunge). You can switch exercises using the app interface.

### Running the Backend Locally

Make sure your FastAPI backend is running before you attempt to upload videos from the mobile app. By default, it listens on port `5001`.

### GPT Integration

* The backend utilizes **GPT** to generate personalized feedback based on the user's form during exercise. After the joint angle data is analyzed, GPT is used to create a detailed report with suggestions for improvement, ensuring users get more than just raw data – they receive actionable feedback in an understandable format.

### Additional Notes

* The **FormAnalyzer** class uses pose detection to extract joint coordinates and calculate angles for key exercise movements. It then compares those angles to ideal values (provided by GPT) and scores the user's performance.
* The backend handles video uploads, processes them for posture evaluation, and returns feedback that includes angles, deviations, and personalized suggestions.
* The app supports one video upload at a time.