import cv2
import numpy as np
import cvzone
from cvzone.PoseModule import PoseDetector
import math

cap = cv2.VideoCapture('pushup.mp4') #change to 0 for webcam if needed

counter = 0
direction = 0
poseDetector = PoseDetector(trackCon=0.8, detectionCon=0.7)
fourcc = cv2.VideoWriter_fourcc(*"MP4V")
out = cv2.VideoWriter("output2.mp4", fourcc, 30.0, (1280, 720))

arm_length_values = []
angle_values = []

mouse_x, mouse_y = -1, -1  
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)

def show_mouse_position(event,x,y,flags,param):
    global mouse_x, mouse_y
    if event == cv2.EVENT_MOUSEMOVE:
        mouse_x,mouse_y = x,y

cv2.namedWindow("Pushup_Window")
cv2.setMouseCallback("Pushup_Window", show_mouse_position)

def calculate_back_angle(hip_center, shoulder_center, nose):
    
    
    hip_center = np.array(hip_center)
    shoulder_center = np.array(shoulder_center)  
    nose = np.array(nose)
    
    # Create vectors using shoulder centers as middle
    #Future implementation can use scapula center(unsure how to implement)
    vector_shoulder_to_hip = hip_center - shoulder_center
    vector_shoulder_to_nose = nose - shoulder_center
    
    # Calculate magnitudes
    magnitude_1 = np.linalg.norm(vector_shoulder_to_hip)
    magnitude_2 = np.linalg.norm(vector_shoulder_to_nose)
    
    # Edge case in case -- Was running into problems
    if magnitude_1 == 0 or magnitude_2 == 0:
        return 90.0
    
    # Normalize vectors & dot product
    vector_1_normalized = vector_shoulder_to_hip / magnitude_1
    vector_2_normalized = vector_shoulder_to_nose / magnitude_2
    dot_product = np.dot(vector_1_normalized, vector_2_normalized)
    dot_product_clamped = np.clip(dot_product, -1.0, 1.0)
    
    # Calculate angle
    angle_radians = np.arccos(dot_product_clamped)
    angle_degrees = math.degrees(angle_radians)
    
    return angle_degrees

def label_back_posture(angle):
    
    if 160 <= angle <= 200:
        return "EXCELLENT", (0, 255, 0)  
    elif 150 <= angle < 160 or 200 < angle <= 210:
        return "GOOD", (0, 255, 255)     
    elif 140 <= angle < 150 or 210 < angle <= 220:
        return "FAIR", (0, 165, 255)     
    else:
        return "POOR", (0, 0, 255)       


def detect_orientation(lmlist):
    if len(lmlist) < 25:
        return "unknown", "center"
    
    left_shoulder = lmlist[11]
    right_shoulder = lmlist[12]
    nose = lmlist[0]
    left_hip = lmlist[23]
    right_hip = lmlist[24]
    
    shoulder_width = abs(left_shoulder[0] - right_shoulder[0])
    
    # Determine general orientation
    if shoulder_width < 80:
        orientation = "side"
    elif shoulder_width > 200:
        orientation = "front"
    else:
        orientation = "diagonal"
    
    # Determine facing direction for front/diagonal orientations
    direction = "center"
    if orientation in ["front", "diagonal"]:
        body_center_x = (left_shoulder[0] + right_shoulder[0]) // 2
        hip_center_x = (left_hip[0] + right_hip[0]) // 2
        torso_center_x = (body_center_x + hip_center_x) // 2
        
        nose_offset = nose[0] - torso_center_x
        
        if nose_offset < -30:  
            direction = "left"
        elif nose_offset > 30:  
            direction = "right"
        else:
            direction = "center" 
    
    return orientation, direction

def angles(lmlist, p1, p2, p3, p4, p5, p6, drawpoints):
    global counter, direction, arm_length_values, angle_values
    
    if len(lmlist) == 0:
        return
        
    # Get points
    point1 = lmlist[p1]  # left shoulder
    point2 = lmlist[p2]  # left elbow  
    point3 = lmlist[p3]  # left wrist
    point4 = lmlist[p4]  # right shoulder
    point5 = lmlist[p5]  # right elbow
    point6 = lmlist[p6]  # right wrist
    
    x1,y1,z1 = point1
    x2,y2,z2 = point2
    x3,y3,z3 = point3    
    x4,y4,z4 = point4
    x5,y5,z5 = point5
    x6,y6,z6 = point6
    
    # Draw points if requested
    if drawpoints:
        points = [(x1,y1), (x2,y2), (x3,y3), (x4,y4), (x5,y5), (x6,y6)]
        for px, py in points:
            cv2.circle(frame, (px,py), 15, (255,255,255), -1)
            cv2.circle(frame, (px,py), 10, (255,0,0), -1)
        
        
        cv2.line(frame,(x1,y1),(x2,y2),(0,0,255),3)    
        cv2.line(frame,(x2,y2),(x3,y3),(0,0,255),3)
        cv2.line(frame,(x4,y4),(x5,y5),(0,0,255),3)
        cv2.line(frame,(x5,y5),(x6,y6),(0,0,255),3)
        cv2.line(frame,(x1,y1),(x4,y4),(0,0,255),3)
    
    
    orientation, facing_direction = detect_orientation(lmlist)
    
    # Calculate centers for form checking
    shoulder_center = np.array([(x1 + x4) // 2, (y1 + y4) // 2])
    hip_center = np.array([(lmlist[23][0] + lmlist[24][0]) // 2, 
                          (lmlist[23][1] + lmlist[24][1]) // 2])
    nose = np.array([lmlist[0][0], lmlist[0][1]])
    
    # FORM CHECKING: Calculate back straightness
    #hip -> shoulder -> nose
    back_angle = calculate_back_angle(hip_center, shoulder_center, nose)
    posture_status, posture_color = label_back_posture(back_angle)
    
    # Draw form checking visualization
    # Draw the vectors used for angle calculation
    cv2.line(frame, tuple(shoulder_center.astype(int)), tuple(hip_center.astype(int)), (255, 255, 0), 3)
    cv2.line(frame, tuple(shoulder_center.astype(int)), tuple(nose.astype(int)), (255, 255, 0), 3)
    
    # Mark the key points
    cv2.circle(frame, tuple(shoulder_center.astype(int)), 8, (255, 255, 0), -1)
    cv2.circle(frame, tuple(hip_center.astype(int)), 8, (255, 255, 0), -1)
    cv2.circle(frame, tuple(nose.astype(int)), 8, (255, 255, 0), -1)
    
    
    left_arm_length = math.sqrt((x3-x1)**2 + (y3-y1)**2)
    right_arm_length = math.sqrt((x6-x4)**2 + (y6-y4)**2)
    avg_arm_length = (left_arm_length + right_arm_length) / 2
    left_arm_angle = math.degrees(math.atan2(y3-y2,x3-x2) - math.atan2(y1-y2,x1-x2))
    right_arm_angle = math.degrees(math.atan2(y6-y5,x6-x5) - math.atan2(y4-y5,x4-x5))
    
    left_arm_angle = abs(left_arm_angle)
    right_arm_angle = abs(right_arm_angle)
    avg_angle = (left_arm_angle + right_arm_angle) / 2
    
    # Store values for adaptive thresholding
    arm_length_values.append(avg_arm_length)
    angle_values.append(avg_angle)
    
    # Keep only recent values
    if len(arm_length_values) > 100:
        arm_length_values = arm_length_values[-100:]
    if len(angle_values) > 100:
        angle_values = angle_values[-100:]
    
    # Calculate adaptive thresholds
    pushup_down = False
    pushup_up = False
    
    if len(arm_length_values) > 20:
        arm_min = min(arm_length_values)
        arm_max = max(arm_length_values)
        arm_range = arm_max - arm_min
        
        arm_down_threshold = arm_min + (arm_range * 0.7)
        arm_up_threshold = arm_min + (arm_range * 0.3)
    else:
        arm_down_threshold = 180
        arm_up_threshold = 150
    
    if len(angle_values) > 20:
        angle_min = min(angle_values)
        angle_max = max(angle_values)
        angle_range = angle_max - angle_min
        
        angle_down_threshold = angle_min + (angle_range * 0.3)
        angle_up_threshold = angle_min + (angle_range * 0.7)
    else:
        angle_down_threshold = 90
        angle_up_threshold = 140
    
    # Orientation specific counting logic
    if orientation == "side":
        pushup_down = avg_angle < angle_down_threshold
        pushup_up = avg_angle > angle_up_threshold
        
    elif orientation == "front":
        if facing_direction == "left":
            left_extension = math.sqrt((x3-x1)**2 + (y3-y1)**2)
            pushup_down = left_extension > (arm_down_threshold * 0.9) or avg_arm_length > (arm_down_threshold * 0.9)
            pushup_up = left_extension < (arm_up_threshold * 1.1) or avg_arm_length < (arm_up_threshold * 1.1)
            
        elif facing_direction == "right":
            right_extension = math.sqrt((x6-x4)**2 + (y6-y4)**2)
            pushup_down = right_extension > (arm_down_threshold * 0.9) or avg_arm_length > (arm_down_threshold * 0.9)
            pushup_up = right_extension < (arm_up_threshold * 1.1) or avg_arm_length < (arm_up_threshold * 1.1)
            
        else:  # center
            pushup_down = avg_arm_length > arm_down_threshold
            pushup_up = avg_arm_length < arm_up_threshold
        
    else:  # diagonal
        angle_factor = avg_angle > angle_up_threshold
        length_factor = avg_arm_length < arm_up_threshold
        
        if facing_direction in ["left", "right"]:
            angle_factor = avg_angle > (angle_up_threshold * 0.9)
            length_factor = avg_arm_length < (arm_up_threshold * 1.1)
            
        pushup_down = not angle_factor and not length_factor
        pushup_up = angle_factor and length_factor
    
    # Update counter
    if pushup_down and direction == 0:
        counter += 0.5
        direction = 1
        
    if pushup_up and direction == 1:
        counter += 0.5
        direction = 0
    
    # Display information
    cv2.putText(frame, f"Count: {int(counter)}", (4,70), cv2.FONT_HERSHEY_PLAIN, 3, (255,255,255), 3)
    cv2.putText(frame, f"Orientation: {orientation}", (4,120), cv2.FONT_HERSHEY_PLAIN, 2, (0,255,0), 2)
    cv2.putText(frame, f"Facing: {facing_direction}", (4,160), cv2.FONT_HERSHEY_PLAIN, 2, (0,255,0), 2)
    
    # Form checking display
    cv2.putText(frame, f"Back Angle: {back_angle:.2f}°", (4,200), cv2.FONT_HERSHEY_PLAIN, 2, (255,255,0), 2)
    cv2.putText(frame, f"Posture: {posture_status}", (4,240), cv2.FONT_HERSHEY_PLAIN, 2, posture_color, 2)
    
    # Rep counting state
    state_color = (0,255,0) if pushup_down else (0,0,255) if pushup_up else (128,128,128)
    state_text = "DOWN" if pushup_down else "UP" if pushup_up else "NEUTRAL"
    cv2.putText(frame, f"State: {state_text}", (4,280), cv2.FONT_HERSHEY_PLAIN, 2, state_color, 2)

while True:
    ret, frame = cap.read()

    if not ret:
        #redundancy check for video end
        cap = cv2.VideoCapture('pushup.mp4')#change to 0 for webcam if needed
        continue

    frame = cv2.resize(frame, (1280,720))
    
    poseDetector.findPose(frame, draw=False)
    lmlist, bbox = poseDetector.findPosition(frame, draw=False, bboxWithHands=False)
    
    angles(lmlist, 11, 13, 15, 12, 14, 16, drawpoints=True)
    out.write(frame)
    cv2.imshow('Pushup_Window', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
out.release()
cv2.destroyAllWindows()