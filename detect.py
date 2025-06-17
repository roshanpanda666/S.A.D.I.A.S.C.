import cv2
import mediapipe as mp
from sound import Playsound1
from message import sendmessage
# Initialize MediaPipe pose detection modules globally
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

# Pose estimation setup
pose = mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5)

# Default sound function — can be switched dynamically
current_sound_function = Playsound1

def detect_persons(frame):
    image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(image_rgb)

    if results.pose_landmarks:
        mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
        return True, frame
    else:
        return False, frame

def run_camera_detection(camera_index=0):
    cap = cv2.VideoCapture(camera_index)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        detected, output_frame = detect_persons(frame)

        label = "Person Detected" if detected else "No Person"
        cv2.putText(output_frame, label, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1,
                    (0, 255, 0) if detected else (0, 0, 255), 2)
        cv2.imshow("Person Detection", output_frame)

        if detected:
            current_sound_function()
            sendmessage()

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# Optional: run directly
if __name__ == "__main__":
    run_camera_detection()
