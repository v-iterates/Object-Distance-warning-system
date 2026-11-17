import cv2
import numpy as np
import math

cap = cv2.VideoCapture(0)

given_distance = 0.15  # input ref meters
k = None
prev_distance = 0
alpha = 0.7

def get_center(mask):
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        if cv2.contourArea(cnt) > 800:
            x, y, w, h = cv2.boundingRect(cnt)
            return (x + w//2, y + h//2), (x, y, w, h)
    return None, None

while True:
    ret, frame = cap.read()
    if not ret:
        break
    frame = cv2.flip(frame, 1)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_red1 = np.array([0,120,70])
    upper_red1 = np.array([10,255,255])
    lower_red2 = np.array([170,120,70])
    upper_red2 = np.array([180,255,255])

    mask_red = cv2.inRange(hsv, lower_red1, upper_red1) + \
               cv2.inRange(hsv, lower_red2, upper_red2)

    lower_blue = np.array([90, 80, 50])
    upper_blue = np.array([140, 255, 255])

    mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)

    kernel = np.ones((5,5), np.uint8)

    mask_red = cv2.morphologyEx(mask_red, cv2.MORPH_OPEN, kernel)
    mask_blue = cv2.morphologyEx(mask_blue, cv2.MORPH_OPEN, kernel)

    red_center, red_box = get_center(mask_red)
    blue_center, blue_box = get_center(mask_blue)
    if red_box:
        x,y,w,h = red_box
        cv2.rectangle(frame, (x,y), (x+w,y+h), (0,0,255), 2)
    if blue_box:
        x,y,w,h = blue_box
        cv2.rectangle(frame, (x,y), (x+w,y+h), (255,0,0), 2)
    if red_center and blue_center:
        x1, y1 = red_center
        x2, y2 = blue_center

        pixel_distance = math.sqrt((x2-x1)**2 + (y2-y1)**2)
        pixel_distance = alpha * prev_distance + (1-alpha) * pixel_distance
        prev_distance = pixel_distance

        cv2.line(frame, red_center, blue_center, (255,255,255), 2)

        if k is None:
            cv2.rectangle(frame, (40,20), (350,80), (0,0,0), -1)
            cv2.putText(frame, "Press C to Calibrate",
            (50,50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2)
        else:
            distance_m = k / pixel_distance if pixel_distance != 0 else 0
            if distance_m < 0.3:
                status = "CRITICAL"
                color = (0,0,255)
            elif distance_m < 0.7:
                status = "WARNING"
                color = (0,165,255)
            else:
                status = "SAFE"
                color = (0,255,0)

            cv2.putText(frame, f"{distance_m:.2f} m",
                        (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

            cv2.putText(frame, status,
                        (50,100), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 3)

    cv2.imshow("Adaptive Distance System", frame)
    key = cv2.waitKey(10) & 0xFF

    if key == ord('c') and red_center and blue_center:
        pixel_distance = math.sqrt(
            (blue_center[0] - red_center[0])**2 +
            (blue_center[1] - red_center[1])**2
        )
        k = given_distance * pixel_distance
        print("Calibration Done. k =", k)
    if key == 27:
        break
    cap.release()
    cv2.destroyAllWindows()
