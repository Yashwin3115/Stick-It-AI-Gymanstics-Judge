import cv2
import mediapipe as mp
from Moves.dance import is_dancing  
from Moves.handstand import is_handstand
from Moves.back_handspring import is_back_handspring
from Moves.cartwheel import is_cartwheel 
from Moves.double_double import is_double_double
from Moves.front_flip import is_front_flip
from Moves.wolf_turn import is_wolf_turn
import math
import warnings

warnings.filterwarnings('ignore', category=DeprecationWarning)

mp_pose = mp.solutions.pose
pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

# Function to calculate the angle between three points
def calculate_angle(a, b, c):
    a = [a.x, a.y]
    b = [b.x, b.y]
    c = [c.x, c.y]

    ab = [a[0] - b[0], a[1] - b[1]]
    bc = [c[0] - b[0], c[1] - b[1]]

    dot_product = ab[0] * bc[0] + ab[1] * bc[1]
    magnitude_ab = math.sqrt(ab[0]**2 + ab[1]**2)
    magnitude_bc = math.sqrt(bc[0]**2 + bc[1]**2)

    cosine_angle = dot_product / (magnitude_ab * magnitude_bc)
    angle = math.acos(cosine_angle)
    return math.degrees(angle)

# Ideal angles for scoring each move (these values are examples, adjust based on expected body alignment)
ideal_angles = {
    "handstand": {"hip_angle": 180, "shoulder_angle": 180},  # Example values
    "back_handspring": {"hip_angle": 130, "knee_angle": 170},  # Example values
    "cartwheel": {"arm_angle": 90},  # Example values
    "double_double": {"shoulder_angle": 180, "hip_angle": 180},  # Example values
    "front_flip": {"knee_angle": 90},  # Example values
    "wolf_turn": {"knee_angle": 120, "hip_angle": 120},  # Example values
    "squat": {"knee_angle": 90},  # Example values
    "plank": {"knee_angle": 180, "hip_angle": 180},  # Example values
}

# Function to calculate score based on angles
def calculate_score(move_name, angles):
    score = 0
    if move_name in ideal_angles:
        for key, ideal_angle in ideal_angles[move_name].items():
            if key in angles:
                angle_diff = abs(angles[key] - ideal_angle)
                # A smaller difference means a better score
                score += max(0, 10 - angle_diff / 10)
    score = min(score, 10)  # Ensure the score doesn't exceed 10
    return score

# Function to classify exercises and calculate angles
def classify_exercise(landmarks):
    angles = {}
    
    if is_handstand(landmarks, mp_pose):
        angles["hip_angle"] = calculate_angle(landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER],
                                              landmarks[mp_pose.PoseLandmark.LEFT_HIP], 
                                              landmarks[mp_pose.PoseLandmark.LEFT_KNEE])
        angles["shoulder_angle"] = calculate_angle(landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER],
                                                  landmarks[mp_pose.PoseLandmark.LEFT_ELBOW],
                                                  landmarks[mp_pose.PoseLandmark.LEFT_WRIST])
        return "Handstand", angles
    elif is_back_handspring(landmarks, mp_pose):
        angles["hip_angle"] = calculate_angle(landmarks[mp_pose.PoseLandmark.LEFT_HIP],
                                              landmarks[mp_pose.PoseLandmark.LEFT_KNEE],
                                              landmarks[mp_pose.PoseLandmark.LEFT_ANKLE])
        angles["knee_angle"] = calculate_angle(landmarks[mp_pose.PoseLandmark.LEFT_KNEE],
                                               landmarks[mp_pose.PoseLandmark.LEFT_ANKLE],
                                               landmarks[mp_pose.PoseLandmark.LEFT_FOOT])
        return "Back Handspring", angles
    elif is_cartwheel(landmarks, mp_pose):
        angles["arm_angle"] = calculate_angle(landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER],
                                              landmarks[mp_pose.PoseLandmark.LEFT_ELBOW],
                                              landmarks[mp_pose.PoseLandmark.LEFT_WRIST])
        return "Cartwheel", angles
    elif is_double_double(landmarks, mp_pose):
        angles["shoulder_angle"] = calculate_angle(landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER],
                                                   landmarks[mp_pose.PoseLandmark.LEFT_ELBOW],
                                                   landmarks[mp_pose.PoseLandmark.LEFT_WRIST])
        angles["hip_angle"] = calculate_angle(landmarks[mp_pose.PoseLandmark.LEFT_HIP],
                                              landmarks[mp_pose.PoseLandmark.LEFT_KNEE],
                                              landmarks[mp_pose.PoseLandmark.LEFT_ANKLE])
        return "Double-Double", angles
    elif is_front_flip(landmarks, mp_pose):
        angles["knee_angle"] = calculate_angle(landmarks[mp_pose.PoseLandmark.LEFT_HIP],
                                               landmarks[mp_pose.PoseLandmark.LEFT_KNEE],
                                               landmarks[mp_pose.PoseLandmark.LEFT_ANKLE])
        return "Front Flip", angles
    elif is_wolf_turn(landmarks, mp_pose):
        angles["knee_angle"] = calculate_angle(landmarks[mp_pose.PoseLandmark.LEFT_HIP],
                                               landmarks[mp_pose.PoseLandmark.LEFT_KNEE],
                                               landmarks[mp_pose.PoseLandmark.LEFT_ANKLE])
        angles["hip_angle"] = calculate_angle(landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER],
                                              landmarks[mp_pose.PoseLandmark.LEFT_HIP],
                                              landmarks[mp_pose.PoseLandmark.LEFT_KNEE])
        return "Wolf Turn", angles
    else:
        return "Unknown Move", {}

# OpenCV to capture video and process each frame
cap = cv2.VideoCapture(0)
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(image)

    if results.pose_landmarks:
        mp.solutions.drawing_utils.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
        exercise, angles = classify_exercise(results.pose_landmarks.landmark)
        score = calculate_score(exercise, angles)
        
        # Display exercise type and score in pink
        cv2.putText(frame, f"Move: {exercise} | Score: {score:.1f}", 
                    (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 105, 180), 2)
    else:
        cv2.putText(frame, "No Move Detected", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    cv2.imshow('Move Classification', frame)

    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
