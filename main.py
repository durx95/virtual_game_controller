import cv2
import mediapipe as mp
from pynput.keyboard import Controller, Key
import time

keyboard = Controller()
last_direction = "Center"
last_press_time = 0
cooldown = 0.15   # prevents multiple fast key presses

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=False,
                    min_detection_confidence=0.6,
                    min_tracking_confidence=0.6)

cap = cv2.VideoCapture(0)

# smoothing variables
smooth_mid_x = 0
smooth_mid_y = 0
alpha = 0.7   # smoothing factor (0.5–0.8 best)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results_pose = pose.process(rgb_frame)

    if results_pose.pose_landmarks:
        mp_drawing.draw_landmarks(frame,
                                  results_pose.pose_landmarks,
                                  mp_pose.POSE_CONNECTIONS)

        x1 = results_pose.pose_landmarks.landmark[11].x * w
        y1 = results_pose.pose_landmarks.landmark[11].y * h
        x2 = results_pose.pose_landmarks.landmark[12].x * w
        y2 = results_pose.pose_landmarks.landmark[12].y * h

        mid_x = int((x1 + x2) // 2)
        mid_y = int((y1 + y2) // 2)

        # 🔥 Smoothing applied
        if smooth_mid_x == 0:
            smooth_mid_x, smooth_mid_y = mid_x, mid_y
        else:
            smooth_mid_x = int(alpha * mid_x + (1 - alpha) * smooth_mid_x)
            smooth_mid_y = int(alpha * mid_y + (1 - alpha) * smooth_mid_y)

        cv2.circle(frame, (smooth_mid_x, smooth_mid_y), 10, (0, 255, 0), -1)

        threshold_x = 40   # reduced for faster response
        threshold_y = 40
        position = "Center"

        if abs(smooth_mid_x - w//2) > threshold_x:
            if smooth_mid_x < w//2:
                position = "Left"
            else:
                position = "Right"

        elif abs(smooth_mid_y - h//2) > threshold_y:
            if smooth_mid_y < h//2:
                position = "Up"
            else:
                position = "Down"

        current_time = time.time()

        # 🔥 cooldown control
        if position != last_direction and current_time - last_press_time > cooldown:

            if position == "Left":
                keyboard.press(Key.left)
                keyboard.release(Key.left)

            elif position == "Right":
                keyboard.press(Key.right)
                keyboard.release(Key.right)

            elif position == "Up":
                keyboard.press(Key.up)
                keyboard.release(Key.up)

            elif position == "Down":
                keyboard.press(Key.down)
                keyboard.release(Key.down)

            last_direction = position
            last_press_time = current_time

        cv2.putText(frame, position, (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1,
                    (255, 0, 0), 2)

    cv2.line(frame, (0, h//2 + 40), (w, h//2 + 40), (0, 0, 255), 2)
    cv2.line(frame, (0, h//2), (w, h//2), (255, 0, 0), 2)
    cv2.line(frame, (int(w//2)-40, 0), (int(w//2)-40, h), (255, 255, 0), 2)
    cv2.line(frame, (int(w//2)+40, 0), (int(w//2)+40, h), (255, 255, 0), 2)

    cv2.imshow('Subway Pose Detection', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()