from fastapi import FastAPI, File, UploadFile, Form
import os
import uvicorn

UPLOAD_FOLDER = "./uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = FastAPI()

@app.post("/analyze")
async def analyze_form(
    exercise: str = Form(...),
    video: UploadFile = File(...)
):
    print("Received analyze request, exercise =", exercise)
    print("Video filename:", video.filename)
    save_path = os.path.join(UPLOAD_FOLDER, video.filename)
    try:
        contents = await video.read()
        with open(save_path, "wb") as f:
            f.write(contents)
        print(f"Saved video to {save_path}")
    except Exception as e:
        print("Error saving file:", e)
        return {"error": "File save failed", "details": str(e)}, 500
    return {"message": f"Saved video to {save_path}", "exercise": exercise}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5001, debug=True)

