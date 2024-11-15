from calculate_angle import calculate_angle

def is_cartwheel(landmarks, mp_pose):
    # Identifying key body landmarks for cartwheel pose
    left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                     landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
    left_hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,
                landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
    left_knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,
                 landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
    left_elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                   landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
    right_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                      landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]

    # Calculate angles for cartwheel pose (for example, angle between elbow, shoulder, and hip)
    shoulder_angle = calculate_angle(left_shoulder, left_hip, left_knee)
    elbow_angle = calculate_angle(left_shoulder, left_elbow, left_knee)

    # Check for conditions that could indicate a cartwheel (may need adjustments based on testing)
    if shoulder_angle < 70 and elbow_angle < 160:
        return True
    return False
