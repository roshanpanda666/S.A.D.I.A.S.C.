import cv2
import mediapipe as mp
import threading
from sound import Playsound1
from message import sendmessage
from keypress import press  # Must return True when stop signal is triggered

# Initialize MediaPipe pose detection
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
pose = mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5)

# Flags to prevent repeated triggers
message_sent = False
sound_played = False

# Current sound function (can be changed from GUI)
current_sound_function = Playsound1

def detect_persons(frame):
    image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(image_rgb)

    if results.pose_landmarks:
        mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
        return True, frame
    else:
        return False, frame


def run_camera_detection(camera_index=0, number=None):
    global message_sent, sound_played

    cap = cv2.VideoCapture(camera_index)

    if not cap.isOpened():
        print(f"❌ Unable to open camera {camera_index}")
        return

    while True:
        ret, frame = cap.read()
        if not ret or frame is None:
            print("⚠️ Frame capture failed")
            break

        detected, output_frame = detect_persons(frame)

        # Draw label and quit instruction
        label = "Person Detected" if detected else "No Person"
        label_color = (0, 255, 0) if detected else (0, 0, 255)
        cv2.putText(output_frame, label, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, label_color, 2)
        cv2.putText(output_frame, "Press Q to close", (10, 65), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (200, 200, 200), 1)

        cv2.imshow("Person Detection", output_frame)

        if detected:
            if not sound_played:
                threading.Thread(target=current_sound_function, daemon=True).start()
                sound_played = True

            if not message_sent and number:
                threading.Thread(target=sendmessage, args=(number,), daemon=True).start()
                message_sent = True
        else:
            sound_played = False
            message_sent = False

        # Exit conditions
        if press() or (cv2.waitKey(10) & 0xFF == ord('q')):
            print("🛑 Detection stopped by press() or 'q'")
            break

    cap.release()
    cv2.destroyAllWindows()
