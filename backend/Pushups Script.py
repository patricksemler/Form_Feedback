import cv2
import numpy as np
from cvzone.PoseModule import PoseDetector
import json
import math

class FormAnalyzer:
    def __init__(self, exercise_type: str, gpt_json_path: str = None, test_json: dict = None):
        """
        Initialize the analyzer
        - exercise_type: e.g., "pushup", "squat", "lunge"
        - gpt_json_path: path to GPT-provided ideal rep JSON
        - test_json: optional hardcoded JSON for testing
        """
        self.exercise_type = exercise_type
        self.pose_detector = PoseDetector(trackCon=0.8, detectionCon=0.7)
        self.counter = 0
        self.direction = 0  # for rep counting

        # Load GPT or test JSON
        if test_json:
            self.gpt_data = test_json
        elif gpt_json_path:
            with open(gpt_json_path, 'r') as f:
                self.gpt_data = json.load(f)
        else:
            raise ValueError("Either gpt_json_path or test_json must be provided.")

    @staticmethod
    def calculate_angle(a, b, c):
        """
        Calculate angle at point b given points a, b, c
        """
        a, b, c = np.array(a), np.array(b), np.array(c)
        ba, bc = a - b, c - b
        cos_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc) + 1e-6)
        cos_angle = np.clip(cos_angle, -1.0, 1.0)
        return np.degrees(np.arccos(cos_angle))

    def extract_joint_coordinates(self, lmlist, joint_name):
        """
        Map joint name to MediaPipe index and return coordinates
        """
        JOINT_MAP = {
            "nose": 0,
            "left_shoulder": 11,
            "right_shoulder": 12,
            "left_elbow": 13,
            "right_elbow": 14,
            "left_wrist": 15,
            "right_wrist": 16,
            "left_hip": 23,
            "right_hip": 24,
            "left_knee": 25,
            "right_knee": 26,
            "left_ankle": 27,
            "right_ankle": 28
        }

        idx = JOINT_MAP.get(joint_name)
        if idx is not None and len(lmlist) > idx:
            return lmlist[idx][:2]  # only x,y
        else:
            return None

    def process_frame(self, lmlist, rep_number=1):
        """
        Process a single frame: calculate angles based on GPT JSON
        """
        if len(lmlist) == 0:
            return None

        angles_result = {}

        ideal_reps = self.gpt_data.get("ideal_reps", [])
        if len(ideal_reps) < rep_number:
            ideal_rep = ideal_reps[0]  # fallback
        else:
            ideal_rep = ideal_reps[rep_number - 1]

        for joint_name, joint_data in ideal_rep["angles"].items():
            if joint_name == "back_angle":
                left_shoulder = self.extract_joint_coordinates(lmlist, "left_shoulder")
                right_shoulder = self.extract_joint_coordinates(lmlist, "right_shoulder")
                left_hip = self.extract_joint_coordinates(lmlist, "left_hip")
                right_hip = self.extract_joint_coordinates(lmlist, "right_hip")
                nose = self.extract_joint_coordinates(lmlist, "nose")

                if None not in [left_shoulder, right_shoulder, left_hip, right_hip, nose]:
                    shoulder_center = [(left_shoulder[0]+right_shoulder[0])//2,
                                       (left_shoulder[1]+right_shoulder[1])//2]
                    hip_center = [(left_hip[0]+right_hip[0])//2,
                                  (left_hip[1]+right_hip[1])//2]
                    angles_result["back_angle"] = self.calculate_angle(hip_center, shoulder_center, nose)
                else:
                    angles_result["back_angle"] = None
            else:
                PARENT_MAP = {
                    "left_elbow": ("left_shoulder", "left_wrist"),
                    "right_elbow": ("right_shoulder", "right_wrist"),
                    "left_knee": ("left_hip", "left_ankle"),
                    "right_knee": ("right_hip", "right_ankle"),
                    "front_knee": ("left_hip", "left_ankle"),
                    "back_knee": ("right_hip", "right_ankle"),
                    "hip_angle": ("left_shoulder", "left_hip"),
                }
                parent_name, child_name = PARENT_MAP.get(joint_name, (None, None))
                joint_coord = self.extract_joint_coordinates(lmlist, joint_name)
                parent_coord = self.extract_joint_coordinates(lmlist, parent_name)
                child_coord = self.extract_joint_coordinates(lmlist, child_name)
                if None not in [parent_coord, joint_coord, child_coord]:
                    angles_result[joint_name] = self.calculate_angle(parent_coord, joint_coord, child_coord)
                else:
                    angles_result[joint_name] = None

        assessment = self.assess_rep_quality(angles_result, rep_number)
        return assessment

    def assess_rep_quality(self, angles: dict, rep_number: int):
        """
        Compare angles to GPT JSON and return deviations & score
        """
        ideal_reps = self.gpt_data.get("ideal_reps", [])
        if len(ideal_reps) < rep_number:
            ideal_rep = ideal_reps[0]
        else:
            ideal_rep = ideal_reps[rep_number - 1]

        ideal_angles = ideal_rep["angles"]
        deviations = {}
        score = 100

        for joint, actual_angle in angles.items():
            if actual_angle is None:
                deviations[joint] = None
                continue

            ideal_range = ideal_angles.get(joint)
            if ideal_range:
                min_val, max_val = ideal_range["min"], ideal_range["max"]
                if actual_angle < min_val:
                    deviations[joint] = actual_angle - min_val
                    score -= abs(actual_angle - min_val)
                elif actual_angle > max_val:
                    deviations[joint] = actual_angle - max_val
                    score -= abs(actual_angle - max_val)

        score = max(0, min(score, 100))
        feedback = ideal_rep.get("notes", "")
        return {
            "rep_number": rep_number,
            "angles": angles,
            "deviations": deviations,
            "score": score,
            "feedback": feedback
        }

    def process_video(self, video_path: str):
        """
        Process an uploaded video and return analysis results per rep
        """
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            raise FileNotFoundError(f"Could not open video: {video_path}")

        rep_number = 1
        results = []

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            frame = cv2.resize(frame, (1280, 720))
            self.pose_detector.findPose(frame, draw=False)
            lmlist, _ = self.pose_detector.findPosition(frame, draw=False, bboxWithHands=False)

            assessment = self.process_frame(lmlist, rep_number)
            if assessment:
                results.append(assessment)

            # TODO: implement rep segmentation logic
            # For now, assume single rep

        cap.release()
        return results


# ---------------------------
# Example usage for testing
# ---------------------------
if __name__ == "__main__":
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

    analyzer = FormAnalyzer(exercise_type="pushup", test_json=TEST_JSON)
    video_path = "/Users/sidharthkanchiraju/Desktop/Coding/Hackathon/HowdyHack2025/TAMUHack2.0/Form_Feedback/backend/pushup.mp4"  # Update with your actual video path

    results = analyzer.process_video(video_path)
    print(json.dumps(results, indent=4))