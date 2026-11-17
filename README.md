# ObjTrack Drone Vision — Colour-Based Object Tracking & Distance Estimation

An exploratory Computer Vision project built using **Python, OpenCV and NumPy**, focused on colour-based object detection, real-time tracking, and reference-based distance estimation.

Developed as a second-semester exploration of computer vision, this project investigates how a camera can identify coloured objects, track their positions, and estimate their relative distance using image processing techniques.

> **Project Status:** Working Prototype · Exploratory Development · First Version

---

## Overview

ObjTrack Drone Vision is a webcam-based visual detection prototype that identifies two coloured reference objects — red and blue — and calculates the pixel distance between their centres.

Using a known physical separation between the two markers, the system performs a simple calibration to estimate their distance from the camera.

The estimated distance is then classified into three safety levels:

- 🔴 **CRITICAL** — Distance below 0.3 metres
- 🟠 **WARNING** — Distance below 0.7 metres
- 🟢 **SAFE** — Distance of 0.7 metres or more

The project explores the fundamentals of camera-based object detection and distance estimation as an initial step towards understanding vision-assisted drone obstacle awareness.

## Objectives

- Understand image processing and colour segmentation.
- Implement real-time object detection using HSV colour spaces.
- Identify and track the centre positions of coloured objects.
- Explore pixel-based distance measurement.
- Implement a simple reference-based calibration mechanism.
- Apply smoothing to reduce fluctuations in distance measurements.
- Display real-time visual feedback and safety classifications.

## Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| OpenCV (`cv2`) | Image processing, camera input, colour detection and visualisation |
| NumPy | Array operations, image masks and morphological processing |
| Math | Euclidean distance calculation |

### Libraries Used

- **OpenCV:** Used for webcam access, BGR-to-HSV conversion, colour thresholding, contour detection, morphological operations, bounding boxes and live display.
- **NumPy:** Used for numerical operations, defining colour thresholds and creating image-processing kernels.
- **Math:** Used to calculate the Euclidean distance between detected object centres.

## How It Works

The system follows a simple computer vision pipeline:

### 1. Camera Input

Captures live video frames through the system webcam using OpenCV.

```python
cap = cv2.VideoCapture(0)
```

The captured frame is flipped horizontally for a more intuitive camera preview.

### 2. Colour Space Conversion

Each frame is converted from BGR (Blue, Green, Red) to HSV (Hue, Saturation, Value).

```python
hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
```

HSV makes colour-based segmentation easier by separating colour information from brightness.

### 3. Colour Segmentation

The system identifies red and blue objects using predefined HSV ranges.

Red requires two separate threshold ranges because red wraps around the beginning and end of the HSV hue scale.

Blue is identified using a single threshold range.

The resulting binary masks isolate the selected colours from the background.

### 4. Noise Reduction

Morphological opening is applied using a 5 × 5 kernel to remove small unwanted regions from the binary masks.

```python
kernel = np.ones((5, 5), np.uint8)

mask_red = cv2.morphologyEx(
    mask_red, cv2.MORPH_OPEN, kernel
)
```

The same operation is applied to the blue mask.

### 5. Object Detection and Tracking

Contours are extracted from the colour masks.

The system filters contours based on a minimum area threshold of 800 pixels and identifies the bounding rectangle of the detected object.

The centre coordinates are calculated as:

\[
C_x=x+\frac{w}{2}, \qquad
C_y=y+\frac{h}{2}
\]

Where:
- \(x,y\) represent the bounding rectangle's top-left coordinates.
- \(w,h\) represent its width and height.

### 6. Pixel Distance Calculation

When both coloured objects are detected, the Euclidean distance between their centres is calculated.

\[
d_p=\sqrt{(x_2-x_1)^2+(y_2-y_1)^2}
\]

Here, \(d_p\) represents the distance in pixels.

### 7. Calibration and Distance Estimation

The prototype uses a reference separation of 0.15 metres between the red and blue markers.

Pressing `C` calculates the calibration constant:

\[
k=D_{ref}\times d_p
\]

Where:
- \(D_{ref}\) = Known reference separation (0.15 m).
- \(d_p\) = Measured pixel separation during calibration.
- \(k\) = Calibration constant.

The estimated distance is subsequently calculated using:

\[
D_{estimated}=\frac{k}{d_p}
\]

This is a simplified proportional estimation model, based on the assumption that the physical separation between the markers remains fixed.

### 8. Distance Smoothing

To reduce fluctuations in consecutive measurements, exponential smoothing is implemented.

\[
d_t=0.7d_{t-1}+0.3d_{current}
\]

Where:
- \(d_t\) = Smoothed pixel distance.
- \(d_{t-1}\) = Previous smoothed measurement.
- \(d_{current}\) = Current pixel measurement.

### 9. Safety Classification

The estimated distance is classified into three categories:

| Estimated Distance | Status |
|---|---|
| Below 0.3 m | 🔴 CRITICAL |
| 0.3 m to below 0.7 m | 🟠 WARNING |
| 0.7 m and above | 🟢 SAFE |

The classification is displayed on the live camera feed using coloured text.

---

## Project Structure

```text
Drone-Vision/
│
├── main.py              # Main computer vision implementation
├── README.md            # Project documentation
└── requirements.txt     # Python dependencies
```

## 🚀 Getting Started

### Prerequisites

- Python 3.x
- A working webcam
- pip package manager

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR-USERNAME/Drone-Vision.git
cd Drone-Vision
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

Alternatively:

```bash
pip install opencv-python numpy
```

### 3. Run the Project

```bash
python main.py
```

### 4. Calibrate the System

1. Place one red and one blue reference marker in front of the camera.
2. Ensure the physical distance between their centres is approximately 15 cm.
3. Allow the system to detect both markers.
4. Press **C** to calibrate.
5. Observe the estimated distance and safety classification.

**Controls:**

| Key | Action |
|---|---|
| C | Calibrate using the reference distance |
| ESC | Exit the application |

---

## Current Limitations

This project is an exploratory prototype and has several limitations:

- Detection is restricted to predefined red and blue colour ranges.
- Performance depends on lighting conditions and camera quality.
- The system currently selects the first contour exceeding the minimum area threshold rather than performing persistent multi-object tracking.
- Distance estimation relies on a simplified calibration model.
- The calibration assumes a fixed physical separation and comparable positioning of the reference markers.
- The system has not been tested with an actual drone or in real flight conditions.
- No autonomous flight control or obstacle avoidance is implemented.

**Important:** The SAFE, WARNING and CRITICAL classifications are experimental visual indicators, not validated collision-risk assessments or flight-safety commands.

## Future Scope

Potential improvements and directions for further exploration:

- Improve object detection through adaptive HSV thresholding.
- Implement multi-object detection and persistent object tracking.
- Explore camera calibration and focal-length-based distance estimation.
- Investigate optical flow for motion detection.
- Estimate object movement and approach velocity.
- Explore stereo vision and monocular depth estimation.
- Integrate depth sensors or LiDAR for more reliable distance measurements.
- Investigate integration with drone platforms and flight controllers.

## Learning Outcomes

This project provided an opportunity to explore:

- Fundamentals of digital image processing.
- BGR and HSV colour spaces.
- Colour segmentation and binary masking.
- Contour detection and bounding-box extraction.
- Morphological image operations.
- Euclidean distance calculations.
- Basic calibration and measurement estimation.
- Real-time image processing using OpenCV.
- Numerical operations with NumPy.

It also highlighted the difference between detecting an object in an image and accurately estimating its physical position in the real world.

---

## About the Project

**Drone Vision** was developed as an individual exploratory Computer Vision project during the second semester of my B.Tech in Computer Science and Engineering (AI & ML).

The project represents an early exploration of image processing, object detection and camera-based distance estimation, with an interest in understanding how computer vision can contribute to drone navigation and obstacle awareness.


---

*This is an educational prototype intended for experimentation and learning. It is not designed or validated for real-world drone navigation or autonomous flight safety.*
