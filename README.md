
# Face Recognition Attendance System

A comprehensive face recognition-based attendance system built with Python, OpenCV, and Streamlit. The system uses machine learning to recognize faces in real-time and automatically track attendance with a beautiful web dashboard.

![System Status](https://img.shields.io/badge/Status-Active-brightgreen)
![Python](https://img.shields.io/badge/Python-3.7+-blue)
![OpenCV](https://img.shields.io/badge/OpenCV-4.0+-red)
![Streamlit](https://img.shields.io/badge/Streamlit-Latest-orange)

## Table of Contents
- [Features](#features)
- [System Requirements](#system-requirements)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage Guide](#usage-guide)
- [Project Structure](#project-structure)
- [Web Dashboard](#web-dashboard)
- [Troubleshooting](#troubleshooting)
- [Performance Tips](#performance-tips)

##  Features

###  Real-time Face Recognition
- Live camera feed with face detection using Haar Cascade
- K-Nearest Neighbors (KNN) algorithm for accurate recognition
- Support for multiple users
- Real-time feedback with voice confirmation
- Background image overlay for professional appearance

###  Unified Web Dashboard
- **Modern Interface:** Beautiful, responsive web design
- **Multi-page Navigation:** Dashboard, User Management, Analytics, Settings
- **Real-time Updates:** Live attendance tracking and statistics
- **Analytics:** Charts, graphs, and trend analysis
- **User Management:** Easy registration and monitoring

### Advanced Analytics
- Daily attendance reports with visual charts
- Individual user statistics and patterns
- Attendance trends over time
- Export functionality for data backup
- Summary metrics and insights

###  System Management
- Automated data synchronization
- Backup and restore functionality
- Fresh start capabilities
- Data validation and error handling

##  System Requirements

### Hardware
- **Camera:** Webcam or USB camera device
- **RAM:** Minimum 4GB (8GB recommended)
- **Storage:** 2GB free disk space
- **Processor:** Intel Core i3 or equivalent

### Software
- **Python:** 3.7 or higher (3.11+ recommended)
- **Operating System:** Windows 10/11 (tested)
- **Camera Drivers:** Compatible webcam drivers

##  Installation

### 1. Activate Virtual Environment
```bash
# The project already has a virtual environment
cd FaceRecognitionAttendanceSystem
.\myenv\Scripts\Activate.ps1  # Windows PowerShell
# or
myenv\Scripts\activate.bat    # Windows Command Prompt
```

### 2. Install Dependencies (if needed)
```bash
pip install opencv-python scikit-learn pandas streamlit numpy pywin32 plotly
```

### 3. Verify Installation
```bash
python -c "import cv2, sklearn, pandas, streamlit, numpy; print('All packages installed successfully!')"
```

##  Quick Start

### Step 1: Add Your First User
```bash
python addFaces.py
```
- Enter the person's name when prompted
- Look at the camera and move your face around
- System collects 100 face samples automatically
- Press 'q' to quit early if needed

### Step 2: Start Face Recognition
```bash
python test.py
```
- Camera window opens with live feed
- Recognized faces show the person's name
- Press **'o'** to mark attendance
- Press **'q'** to quit

### Step 3: Launch Web Dashboard
```bash
streamlit run unified_dashboard.py
```
- Opens at http://localhost:8501
- Navigate between Dashboard, Users, Analytics, Settings

##  Usage Guide

### Adding New Users

1. **Run face collection:**
   ```bash
   python addFaces.py
   ```

2. **Follow the prompts:**
   - Enter person's name
   - Position face in camera view
   - System automatically collects 100 samples
   - Move face slowly for better coverage

3. **Tips for best results:**
   - Use consistent lighting
   - Face camera directly
   - Avoid extreme angles
   - Remove glasses during training

### Taking Attendance

1. **Start recognition system:**
   ```bash
   python test.py
   ```

2. **Camera operation:**
   - Green rectangle around detected faces
   - Name appears above recognized faces
   - Background overlay for professional look

3. **Mark attendance:**
   - Press **'o'** when correct name appears
   - Voice confirmation: "Attendance Taken!"
   - Record saved to `Attendance/Attendance_DD-MM-YY.csv`

### Web Dashboard Features

####  Dashboard Page
- Today's attendance records
- Quick statistics and metrics
- System status monitoring
- Quick action buttons

#### 👥 User Management
- View all registered users: **Akshita, Anshita, Papa, Mumma**
- Add new users with step-by-step instructions
- Monitor user status and activity
- Reset system data options

#### Analytics
- Visual charts showing attendance patterns
- Daily trends and statistics
- Individual user analytics
- Historical data overview

####  Settings
- System information and diagnostics
- Data management tools
- Backup and export options
- Reset and fresh start functionality

##  Project Structure

```
FaceRecognitionAttendanceSystem/
│
├── 📜 addFaces.py              # Face data collection script
├── 📜 test.py                  # Main face recognition system  
├── 📜 app.py                   # Simple attendance viewer
├── 📜 unified_dashboard.py     # Complete web dashboard
├── 📜 README.md               # Documentation
│
├── 📁 data/                   # Training data and models
│   ├── faces_data.pkl         # Face training data (500 samples)
│   ├── names.pkl              # User names data
│   ├── haarcascade_frontalface_default.xml
│   └── backup*/               # Backup directories
│
├── 📁 Attendance/             # Attendance records
│   └── Attendance_15-08-25.csv  # Daily attendance files
│
├── 📁 myenv/                  # Python virtual environment
└── 🖼️ background.png          # Camera overlay background
```

##  Web Dashboard

The unified dashboard provides a complete interface for managing your attendance system:

### Navigation Features
- **Sidebar Navigation:** Easy switching between pages
- **System Status:** Real-time monitoring in sidebar
- **Responsive Design:** Works on desktop and mobile

### Current System Status
- **👥 Trained Users:** 4 people (Akshita, Anshita, Papa, Mumma)
- **📊 Face Samples:** 500 total samples
- **✅ Data Status:** Synchronized and healthy
- **📅 Active Records:** Daily attendance tracking

## 🛠️ Troubleshooting

### Camera Issues
```bash
# Test camera
python -c "import cv2; cap = cv2.VideoCapture(0); print('Camera OK' if cap.read()[0] else 'Camera Error')"
```

### Face Not Recognized
- Check lighting conditions
- Ensure face is clearly visible
- Retrain user if accuracy is poor
- Verify user exists in training data

### Data Synchronization Issues
```bash
# Check data consistency
python -c "import pickle; faces = pickle.load(open('data/faces_data.pkl', 'rb')); names = pickle.load(open('data/names.pkl', 'rb')); print(f'Faces: {len(faces)}, Names: {len(names)}, Synced: {len(faces) == len(names)}')"
```

### Fresh Start (Reset System)
```bash
# Backup current data first, then remove training files
# Use the Settings page in the dashboard for guided reset
```

## 🚀 Performance Tips

1. **Optimal Environment:**
   - Use consistent, good lighting
   - Minimize background movement
   - Position camera at eye level

2. **Training Quality:**
   - Collect samples with various angles
   - Include different expressions
   - Ensure consistent lighting during training

3. **System Optimization:**
   - Close unnecessary applications
   - Use good quality webcam
   - Keep training data updated


## 🔄 Commands Reference

```bash
# Face recognition system
python test.py                    # Start camera recognition

# User management  
python addFaces.py               # Add new person

# Web interfaces
streamlit run app.py             # Simple viewer
streamlit run unified_dashboard.py  # Full dashboard

# Data verification
python -c "import pickle; print('System OK')"  # Quick health check
```

## 📞 Support

- **System Status:** Check the unified dashboard
- **Data Issues:** Use the Settings page for diagnostics  
- **Recognition Problems:** Retrain users with better lighting
- **Technical Issues:** Review troubleshooting section

---

**🎯 Face Recognition Attendance System** | Built with Python, OpenCV & Streamlit

*Smart attendance tracking for the modern era!*
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    pip install -r requirements.txt
```
***Note:*** If requirements.txt is not provided, you can manually install the required packages:
```bash
pip install opencv-python numpy dlib pandas face_recognition streamlit
```
3. Set Up the Project
- Ensure you have the Haar Cascade file (haarcascade_frontalface_default.xml) in the project directory.
- Place your dataset images in the data directory.
- Run add_faces.py to add faces to the recognition system.

4. Run the Application
To start the attendance system, execute:
```bash
python app.py
```

To view the attendance data in the Streamlit interface, execute:

```bash
streamlit run app.py

```

## Usage 

1. **Add Faces:** Run add_faces.py to add images of individuals to the system.
2. **Start Attendance System:** Run app.py to start capturing video and marking attendance.
3. ***View Attendance:*** Access the Streamlit app to view the attendance records.


## Contributing

Contributions are always welcome!

Feel free to fork the repository and make changes. For major updates or contributions, please open an issue or submit a pull request.

Please adhere to this project's `code of conduct`.

