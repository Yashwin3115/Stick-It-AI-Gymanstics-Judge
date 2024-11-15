from calculate_angle import calculate_angle

def is_double_double(landmarks, mp_pose):
    left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                     landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
    left_hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,
                landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
    left_knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,
                 landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]

    # Check for angles that might signify a double backflip with twists
    hip_angle = calculate_angle(left_shoulder, left_hip, left_knee)
    knee_angle = calculate_angle(left_hip, left_knee, 
                                 [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,
                                  landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y])

    # Basic conditions for a double backflip with twists (example conditions)
    return 70 <= hip_angle <= 160 and knee_angle < 90
