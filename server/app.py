from flask import Flask, request, jsonify
import os

UPLOAD_FOLDER = "./uploads"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = Flask(__name__)

@app.route("/analyze", methods=["POST"])
def analyze_form():
  name = request.form.get("exercise")
  video = request.files.get("video")

  if not video:
     print("No video uploaded")
     return f"No video uploaded, {name}", 400

  savePath = os.path.join(UPLOAD_FOLDER, video.filename)

  video.save(savePath)
  print(f"Saved videon{name}")

  return f"Saved video to {savePath}", 200

if __name__ == "__main__":
    app.run(debug=True)
