from calculate_angle import calculate_angle

def is_front_flip(landmarks, mp_pose):
    left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                     landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
    left_hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,
                landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
    left_knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,
                 landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
    left_ankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,
                  landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]
    
    # Calculate the angle between hip and knee for a tuck position
    knee_angle = calculate_angle(left_hip, left_knee, left_ankle)
    hip_angle = calculate_angle(left_shoulder, left_hip, left_knee)

    # A front flip has a knee angle < 90 and a hip angle < 90 during the flip
    return knee_angle < 90 and hip_angle < 90
