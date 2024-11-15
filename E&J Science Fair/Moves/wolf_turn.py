from calculate_angle import calculate_angle

def is_wolf_turn(landmarks, mp_pose):
    left_knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,
                 landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
    left_ankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,
                  landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]
    left_hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,
                landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
    left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                     landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]

    # Calculate knee angle for a "bent knee" position
    knee_angle = calculate_angle(left_hip, left_knee, left_ankle)
    torso_angle = calculate_angle(left_shoulder, left_hip, left_knee)

    # Wolf turn likely involves knee angle < 90 and a torso angle around 90 for balance
    return knee_angle < 90 and 80 <= torso_angle <= 100
