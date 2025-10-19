from flask import Flask, request, jsonify
from flask_cors import CORS
import os
# from form_analyzer import FormAnalyzer  # Import your FormAnalyzer class

UPLOAD_FOLDER = "./uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = Flask(__name__)
CORS(app)  # Enable CORS for React Native frontend

# Example JSON for testing (move to a file or database later)
TEST_JSON = {
    "exercise": "pushup",
    "ideal_reps": [
        {
            "rep_number": 1,
            "angles": {
                "left_elbow": {"min": 80, "max": 100},
                "right_elbow": {"min": 80, "max": 100},
                "back_angle": {"min": 165, "max": 180}
            },
            "notes": "Keep back straight, elbows close, controlled descent"
        }
    ]
}

@app.route("/analyze", methods=["POST"])
def analyzeform():
    exercise = request.form.get("exercise")
    video = request.files.get("video")

    if not video or not exercise:
        print("Missing video or exercise")
        return jsonify({"error": f"No video or exercise provided, got exercise: {exercise}"}), 400

  savePath = os.path.join(UPLOAD_FOLDER, video.filename)

  video.save(savePath)
  print(f"Saved videon{name}")

  return f"Saved video to {savePath}", 200

if __name__ == "__main__":
    app.run(debug=True)
