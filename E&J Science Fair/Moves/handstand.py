from calculate_angle import calculate_angle

def is_handstand(landmarks, mp_pose):
    left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                     landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
    left_hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,
                landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
    left_ankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,
                  landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]

    # Calculate angles to determine if the body is in an inverted (handstand) position
    shoulder_hip_angle = calculate_angle(left_shoulder, left_hip, left_ankle)

    # Check if the body is straight up (close to 180 degrees) for a handstand
    return 160 <= shoulder_hip_angle <= 180
