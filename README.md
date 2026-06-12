# 👁️ Eye Gaze Mouse Control System using MediaPipe

> A low-cost, webcam-based eye gaze mouse control system with blink detection and low-light robustness — implemented in Python using Google MediaPipe FaceMesh.

---

## 📄 Research Paper

**Title:** A Low-Cost Webcam-Based Eye Gaze Mouse Control System with Blink Detection and Low-Light Robustness Using MediaPipe

**Journal:** International Journal of Advanced Computer Science and Applications (IJACSA) — Scopus Indexed

**Submission ID:** MS-17-7-0379 | Vol. 17 · Issue 7 · 2026

---

## 🎯 Project Overview

This system allows physically disabled individuals to control a computer mouse using only their eyes — no special hardware required, just a standard laptop webcam.

The system was developed as a BSCS Final Year Project at CECOS University of IT and Emerging Sciences, Peshawar, Pakistan.

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 👁️ **Iris Cursor Control** | Move mouse cursor using eye/iris movement |
| 😉 **Blink Click Detection** | Left wink = Left click, Right wink = Right click |
| 📜 **Dwell Scrolling** | Look up/down zones to scroll |
| 🌙 **Low-Light Robustness** | CLAHE preprocessing for dim environments |
| 🎯 **False Click Prevention** | 10-frame temporal filter + 2s cooldown |
| 💰 **Zero Hardware Cost** | Works with any standard 720p webcam |

---

## 📊 Performance Results

| Metric | Result |
|--------|--------|
| Cursor Accuracy | 75.5% (SD = 9.6) |
| Click Accuracy | 72.0% (SD = 14.0) |
| Scroll Accuracy | 76.0% (SD = 14.3) |
| False Click Reduction | 79.5% |
| CLAHE Improvement (Dim) | +17.7% |
| ANOVA (Lighting Effect) | F = 9.66, p = 0.0097 ✅ |

---

## 🛠️ Requirements

### Hardware
- Standard laptop or USB webcam (720p minimum)
- No GPU required

### Software
```
Python 3.8+
mediapipe
opencv-python
pyautogui
numpy
```

Install all dependencies:
```bash
pip install mediapipe opencv-python pyautogui numpy
```

---

## 🚀 How to Run

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/eye-gaze-mouse-control.git

# Go into the folder
cd eye-gaze-mouse-control

# Install requirements
pip install -r requirements.txt

# Run the system
python eye_gaze_control.py
```

---

## 🔧 System Architecture

The system runs a **6-stage real-time pipeline:**

```
📷 Webcam Input
      ↓
🌙 CLAHE Preprocessing (Low-light enhancement)
      ↓
🤖 MediaPipe FaceMesh (478 facial landmarks)
      ↓
👁️ Iris Detection & Screen Mapping
      ↓
😉 EAR Blink Detection (10-frame filter)
      ↓
🖱️ Mouse Action (Move / Click / Scroll)
```

---

## ⚙️ Configuration

| Parameter | Value | Description |
|-----------|-------|-------------|
| EAR Threshold | 0.08 | Blink detection sensitivity |
| EMA Alpha | 0.08 | Cursor smoothing factor |
| Cooldown | 2.0s | Anti-false-click delay |
| Scroll Zone | 8% top/bottom | Dwell scroll trigger area |
| CLAHE Clip Limit | 3.0 | Contrast enhancement strength |
| Grid Size | 8×8 | CLAHE tile grid |

---

## 🧪 Tested On

- ✅ Windows 10 / 11
- ✅ Python 3.9, 3.10
- ✅ Standard 720p laptop webcam
- ✅ Bright, Moderate, and Dim lighting conditions
- ✅ 10 participants (CECOS University, Peshawar)

---

## 📁 Project Structure

```
eye-gaze-mouse-control/
│
├── eye_gaze_control.py      # Main system file
├── requirements.txt         # Python dependencies
├── README.md                # This file
└── paper/
    └── paper.pdf            # Research paper (published version)
```

---

## 🔬 Comparison with Existing Systems

| System | Accuracy | Low-Light | False Clicks | Cost |
|--------|----------|-----------|--------------|------|
| Tobii Eye Tracker 5 | 95.0% | ✅ | < 2% | $250+ |
| Rajpurkar et al. | 84.3% | ❌ | 34.0% | $0 |
| NeuGaze | 86.1% | ❌ | 18.3% | $0 |
| **This System** | **75.5%** | **✅** | **6.7%** | **$0** |

---

## ⚠️ Limitations

- Sample size: 10 participants (preliminary study)
- No per-user EAR calibration yet
- Performance may vary with extreme eye geometries

---

## 🔮 Future Work

- Per-user EAR calibration
- Infrared lighting support
- Fatigue detection
- Evaluation on participants with motor disabilities
- Expanded participant pool (n ≥ 30)

---

## 👤 Author

**Fahad Ahmad**
BSCS Final Year — CECOS University of IT and Emerging Sciences, Peshawar, Pakistan
📧 fahadk8451011@gmail.com

---

## 📜 License

This project is open source under the [MIT License](LICENSE).

---

## 🙏 Acknowledgements

- [Google MediaPipe](https://mediapipe.dev/) — FaceMesh framework
- [CLAHE](https://en.wikipedia.org/wiki/Adaptive_histogram_equalization) — Zuiderveld, Graphics Gems IV, 1994
- CECOS University — for research support and participant recruitment
