"""
Eye Gaze Computer Control System 
Requirements:
Author : [Fahad Ahmad]
Topic  : Webcam-Based Eye Gaze Mouse Control System
"""

import cv2
import mediapipe as mp
import pyautogui
import numpy as np
import time

pyautogui.FAILSAFE = False
pyautogui.PAUSE    = 0

mp_face_mesh = mp.solutions.face_mesh
face_mesh    = mp_face_mesh.FaceMesh(
    max_num_faces            = 1,
    refine_landmarks         = True,
    min_detection_confidence = 0.7,
    min_tracking_confidence  = 0.7
)

SCREEN_W, SCREEN_H = pyautogui.size()

LEFT_IRIS  = [474, 475, 476, 477]
RIGHT_IRIS = [469, 470, 471, 472]

LEFT_EYE_TOP    = [159, 160, 161]
LEFT_EYE_BOTTOM = [145, 144, 163]
LEFT_EYE_LEFT   = 33
LEFT_EYE_RIGHT  = 133

RIGHT_EYE_TOP    = [386, 385, 384]
RIGHT_EYE_BOTTOM = [374, 373, 380]
RIGHT_EYE_LEFT   = 362
RIGHT_EYE_RIGHT  = 263

# ── CALIBRATED FOR YOUR EYES (L-EAR natural = 0.24) ──
SMOOTHING       = 8
BLINK_THRESH    = 0.08   # Well below your natural 0.24 — only real wink triggers
BLINK_CONSEC    = 10     # Must hold for 10 frames
BLINK_COOLDOWN  = 2.0    # 2 seconds between clicks
DWELL_ZONE_TOP  = 0.08
DWELL_ZONE_BOT  = 0.92
DWELL_TIME      = 2.0
SCROLL_AMOUNT   = 300
SCROLL_COOLDOWN = 1.0
CURSOR_MARGIN   = 0.12

prev_x, prev_y        = SCREEN_W // 2, SCREEN_H // 2
left_blink_counter    = 0
right_blink_counter   = 0
left_blink_total      = 0
right_blink_total     = 0
last_left_click_time  = 0
last_right_click_time = 0
dwell_start           = None
last_scroll_time      = 0


def enhance_low_light(frame):
    lab     = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    clahe   = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    l_eq    = clahe.apply(l)
    lab_eq  = cv2.merge([l_eq, a, b])
    return cv2.cvtColor(lab_eq, cv2.COLOR_LAB2BGR)


def get_iris_center(landmarks, indices, fw, fh):
    pts = [(int(landmarks[i].x * fw), int(landmarks[i].y * fh)) for i in indices]
    return int(np.mean([p[0] for p in pts])), int(np.mean([p[1] for p in pts]))


def ear(landmarks, top_ids, bot_ids, left_id, right_id, fw, fh):
    top = np.array([(landmarks[i].x * fw, landmarks[i].y * fh) for i in top_ids])
    bot = np.array([(landmarks[i].x * fw, landmarks[i].y * fh) for i in bot_ids])
    lp  = np.array([landmarks[left_id].x  * fw, landmarks[left_id].y  * fh])
    rp  = np.array([landmarks[right_id].x * fw, landmarks[right_id].y * fh])
    v   = np.mean(np.linalg.norm(top - bot, axis=1))
    h   = np.linalg.norm(lp - rp)
    return v / h if h != 0 else 0.3


def smooth(nx, ny, px, py, a):
    return int(px + (nx - px) / a), int(py + (ny - py) / a)


def iris_to_screen(ix, iy, fw, fh):
    mx = int(fw * CURSOR_MARGIN)
    my = int(fh * CURSOR_MARGIN)
    ix = np.clip(ix, mx, fw - mx)
    iy = np.clip(iy, my, fh - my)
    sx = int((ix - mx) / (fw - 2 * mx) * SCREEN_W)
    sy = int((iy - my) / (fh - 2 * my) * SCREEN_H)
    return np.clip(sx, 0, SCREEN_W-1), np.clip(sy, 0, SCREEN_H-1)


def main():
    global prev_x, prev_y
    global left_blink_counter, right_blink_counter
    global left_blink_total, right_blink_total
    global last_left_click_time, last_right_click_time
    global dwell_start, last_scroll_time

    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH,  640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    print("=" * 55)
    print("  EYE GAZE CONTROL — FINAL VERSION  [Q = Quit]")
    print("=" * 55)
    print("  • Gaze       → Cursor move")
    print("  • Left Wink  → Left Click  (2s cooldown)")
    print("  • Right Wink → Right Click (2s cooldown)")
    print("  • Look UP    → Scroll Up   (1.5s hold)")
    print("  • Look DOWN  → Scroll Down (1.5s hold)")
    print("=" * 55)

    while True:
        ret, frame = cap.read()
        if not ret:
            print("[ERROR] Webcam failed.")
            break

        fh, fw = frame.shape[:2]
        frame_rgb = cv2.cvtColor(enhance_low_light(frame), cv2.COLOR_BGR2RGB)
        results   = face_mesh.process(frame_rgb)

        if results.multi_face_landmarks:
            lm = results.multi_face_landmarks[0].landmark

            lx, ly = get_iris_center(lm, LEFT_IRIS,  fw, fh)
            rx, ry = get_iris_center(lm, RIGHT_IRIS, fw, fh)
            ax, ay = (lx+rx)//2, (ly+ry)//2

            tx, ty = iris_to_screen(ax, ay, fw, fh)
            sx, sy = smooth(tx, ty, prev_x, prev_y, SMOOTHING)
            pyautogui.moveTo(sx, sy)
            prev_x, prev_y = sx, sy

            l_ear = ear(lm, LEFT_EYE_TOP,  LEFT_EYE_BOTTOM,
                        LEFT_EYE_LEFT,  LEFT_EYE_RIGHT,  fw, fh)
            r_ear = ear(lm, RIGHT_EYE_TOP, RIGHT_EYE_BOTTOM,
                        RIGHT_EYE_LEFT, RIGHT_EYE_RIGHT, fw, fh)

            lc = l_ear < BLINK_THRESH
            rc = r_ear < BLINK_THRESH
            now = time.time()

            # Left wink → Left click
            if lc and not rc:
                left_blink_counter += 1
                if left_blink_counter == BLINK_CONSEC and now - last_left_click_time > BLINK_COOLDOWN:
                    pyautogui.click(button='left')
                    left_blink_total += 1
                    last_left_click_time = now
                    print(f"  [LEFT CLICK] Total: {left_blink_total}")
            else:
                left_blink_counter = 0

            # Right wink → Right click
            if rc and not lc:
                right_blink_counter += 1
                if right_blink_counter == BLINK_CONSEC and now - last_right_click_time > BLINK_COOLDOWN:
                    pyautogui.click(button='right')
                    right_blink_total += 1
                    last_right_click_time = now
                    print(f"  [RIGHT CLICK] Total: {right_blink_total}")
            else:
                right_blink_counter = 0

            # Dwell scroll
            ny      = ay / fh
            up      = ny < DWELL_ZONE_TOP
            down    = ny > DWELL_ZONE_BOT

            if up or down:
                if dwell_start is None:
                    dwell_start = now
                elif now - dwell_start >= DWELL_TIME and now - last_scroll_time >= SCROLL_COOLDOWN:
                    pyautogui.scroll(SCROLL_AMOUNT if up else -SCROLL_AMOUNT)
                    print("  [SCROLL UP]" if up else "  [SCROLL DOWN]")
                    last_scroll_time = now
                    dwell_start = now
            else:
                dwell_start = None

            # Display
            cv2.circle(frame, (lx, ly), 3, (0, 255, 0), -1)
            cv2.circle(frame, (rx, ry), 3, (0, 255, 0), -1)

            ty_top = int(fh * DWELL_ZONE_TOP)
            ty_bot = int(fh * DWELL_ZONE_BOT)
            cv2.rectangle(frame, (0, 0),        (fw, ty_top), (0, 100, 255), 2)
            cv2.rectangle(frame, (0, ty_bot),   (fw, fh),     (0, 100, 255), 2)
            cv2.putText(frame, "SCROLL UP",   (10, ty_top-5),  cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,100,255), 1)
            cv2.putText(frame, "SCROLL DOWN", (10, ty_bot+15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,100,255), 1)
            cv2.putText(frame, f"L-EAR: {l_ear:.2f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,255), 2)
            cv2.putText(frame, f"R-EAR: {r_ear:.2f}", (10, 55), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,255), 2)
            cv2.putText(frame, f"Cursor:({sx},{sy})",  (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200,200,200), 1)

            if dwell_start:
                prog  = min((now - dwell_start) / DWELL_TIME, 1.0)
                bar_w = int(fw * prog)
                cv2.rectangle(frame, (0, fh-12), (bar_w, fh), (0, 255, 200), -1)

        else:
            cv2.putText(frame, "No Face — Adjust Camera", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        cv2.imshow("Eye Gaze Control — FINAL  [Q=Quit]", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    print("\n[INFO] System stopped.")


if __name__ == "__main__":
    main()
