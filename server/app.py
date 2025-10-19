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

    # Generate unique filename to avoid conflicts
    filename = f"{exercise}{int(time.time())}.mp4"
    save_path = os.path.join(UPLOAD_FOLDER, filename)

    # Save the video
    video.save(save_path)
    print(f"Saved video: {save_path}, exercise: {exercise}")

    try:
        # Initialize FormAnalyzer and process the video
        analyzer = FormAnalyzer(exercise_type=exercise, test_json=TEST_JSON)
        results = analyzer.process_video(save_path)

        return jsonify({
            "message": f"Video saved and analyzed: {save_path}",
            "analysis": results
        }), 200
    except Exception as e:
        print(f"Analysis error: {str(e)}")
        return jsonify({"error": f"Analysis failed: {str(e)}"}), 500

if __name__ == "main":
    app.run(host="0.0.0.0", port=5000, debug=True)