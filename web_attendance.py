import streamlit as st
import cv2
import pickle
import numpy as np
import pandas as pd
import time
import os
import csv
from datetime import datetime
from sklearn.neighbors import KNeighborsClassifier
import threading
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase, RTCConfiguration
import av

# Page configuration
st.set_page_config(
    page_title="Face Recognition Attendance - Web Capture",
    page_icon="📷",
    layout="wide"
)

st.title("📷 Live Face Recognition Attendance")
st.markdown("---")

# Load face recognition data
@st.cache_data
def load_face_data():
    try:
        with open('data/names.pkl', 'rb') as f:
            names = pickle.load(f)
        with open('data/faces_data.pkl', 'rb') as f:
            faces = pickle.load(f)
        return names, faces
    except FileNotFoundError:
        st.error("Face recognition data not found. Please run addFaces.py first.")
        return None, None

# Initialize face detection
@st.cache_resource
def load_face_detector():
    return cv2.CascadeClassifier('data/haarcascade_frontalface_default.xml')

# Initialize KNN model
@st.cache_resource
def load_knn_model():
    names, faces = load_face_data()
    if names is not None and faces is not None:
        knn = KNeighborsClassifier(n_neighbors=5)
        knn.fit(faces, names)
        return knn
    return None

class FaceRecognitionTransformer(VideoTransformerBase):
    def __init__(self):
        self.face_detector = load_face_detector()
        self.knn_model = load_knn_model()
        self.last_detection = None
        self.detection_time = None
        self.confidence_threshold = 0.6

    def transform(self, frame):
        img = frame.to_ndarray(format="bgr24")
        
        if self.knn_model is None:
            cv2.putText(img, "No trained model found", (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            return img
        
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = self.face_detector.detectMultiScale(gray, 1.3, 5)
        
        for (x, y, w, h) in faces:
            # Extract face region
            face_roi = img[y:y+h, x:x+w]
            resized_face = cv2.resize(face_roi, (50, 50)).flatten().reshape(1, -1)
            
            # Predict
            prediction = self.knn_model.predict(resized_face)
            probabilities = self.knn_model.predict_proba(resized_face)
            confidence = np.max(probabilities)
            
            name = prediction[0] if confidence > self.confidence_threshold else "Unknown"
            
            # Draw rectangle and name
            color = (0, 255, 0) if name != "Unknown" else (0, 0, 255)
            cv2.rectangle(img, (x, y), (x+w, y+h), color, 2)
            
            # Add name and confidence
            label = f"{name} ({confidence:.2f})"
            cv2.putText(img, label, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
            
            # Store detection for attendance
            if name != "Unknown" and confidence > 0.8:
                self.last_detection = name
                self.detection_time = datetime.now()
        
        return img

# Load data
names, faces = load_face_data()
if names is None or faces is None:
    st.stop()

# Sidebar controls
st.sidebar.header("📋 Attendance Controls")

# Real-time camera feed
st.header("📹 Live Camera Feed")

# WebRTC configuration
RTC_CONFIGURATION = RTCConfiguration(
    {"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
)

# Create the video transformer
ctx = webrtc_streamer(
    key="face-recognition",
    video_transformer_factory=FaceRecognitionTransformer,
    rtc_configuration=RTC_CONFIGURATION,
    media_stream_constraints={"video": True, "audio": False},
    async_processing=True,
)

# Attendance controls
if ctx.video_transformer:
    st.sidebar.subheader("🎯 Current Detection")
    
    if ctx.video_transformer.last_detection:
        detected_name = ctx.video_transformer.last_detection
        detection_time = ctx.video_transformer.detection_time
        
        st.sidebar.success(f"**Detected:** {detected_name}")
        st.sidebar.info(f"**Time:** {detection_time.strftime('%H:%M:%S')}")
        
        # Attendance button
        if st.sidebar.button("✅ Mark Attendance", type="primary"):
            # Save attendance
            ts = time.time()
            date = datetime.fromtimestamp(ts).strftime("%d-%m-%y")
            timestamp = datetime.fromtimestamp(ts).strftime("%H:%M-%S")
            
            attendance_file = f"Attendance/Attendance_{date}.csv"
            attendance_data = [detected_name, timestamp]
            
            # Check if file exists
            file_exists = os.path.isfile(attendance_file)
            
            try:
                if file_exists:
                    # Append to existing file
                    with open(attendance_file, "a", newline='') as csvfile:
                        writer = csv.writer(csvfile)
                        writer.writerow(attendance_data)
                else:
                    # Create new file with headers
                    with open(attendance_file, "w", newline='') as csvfile:
                        writer = csv.writer(csvfile)
                        writer.writerow(["NAME", "TIME"])
                        writer.writerow(attendance_data)
                
                st.sidebar.success(f"✅ Attendance marked for {detected_name}!")
                st.balloons()
                
            except Exception as e:
                st.sidebar.error(f"Error saving attendance: {str(e)}")
    else:
        st.sidebar.info("👁️ Looking for faces...")

# Display current attendance
st.header("📊 Today's Attendance")

# Get today's date
today_date = datetime.now().strftime("%d-%m-%y")
attendance_file = f"Attendance/Attendance_{today_date}.csv"

if os.path.exists(attendance_file):
    try:
        df = pd.read_csv(attendance_file)
        if not df.empty:
            st.dataframe(df, use_container_width=True)
            
            # Statistics
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Records", len(df))
            with col2:
                if 'NAME' in df.columns:
                    unique_people = df['NAME'].nunique()
                    st.metric("Unique People", unique_people)
            with col3:
                st.metric("Date", today_date)
        else:
            st.info("No attendance records for today yet.")
    except Exception as e:
        st.error(f"Error reading attendance file: {str(e)}")
else:
    st.info("No attendance file for today. Start marking attendance!")

# Manual attendance section
st.header("✏️ Manual Attendance Entry")
with st.expander("Add attendance manually"):
    col1, col2 = st.columns(2)
    
    with col1:
        # Get available names from training data
        available_names = list(set(names))
        selected_name = st.selectbox("Select Person", available_names)
    
    with col2:
        manual_time = st.time_input("Time", datetime.now().time())
    
    if st.button("➕ Add Manual Entry"):
        ts = time.time()
        date = datetime.fromtimestamp(ts).strftime("%d-%m-%y")
        manual_timestamp = manual_time.strftime("%H:%M-%S")
        
        attendance_file = f"Attendance/Attendance_{date}.csv"
        attendance_data = [selected_name, manual_timestamp]
        
        file_exists = os.path.isfile(attendance_file)
        
        try:
            if file_exists:
                with open(attendance_file, "a", newline='') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(attendance_data)
            else:
                with open(attendance_file, "w", newline='') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(["NAME", "TIME"])
                    writer.writerow(attendance_data)
            
            st.success(f"✅ Manual attendance added for {selected_name}!")
            st.rerun()
            
        except Exception as e:
            st.error(f"Error adding manual attendance: {str(e)}")

# Instructions
with st.expander("📖 How to Use"):
    st.markdown("""
    **Live Attendance:**
    1. Allow camera access when prompted
    2. Position your face in front of the camera
    3. When your name appears with high confidence, click "Mark Attendance"
    4. Attendance will be automatically saved
    
    **Manual Entry:**
    - Use this for backup or when camera is not available
    - Select the person and time, then click "Add Manual Entry"
    
    **Tips:**
    - Ensure good lighting for better recognition
    - Face the camera directly
    - Wait for high confidence detection before marking attendance
    """)

# Auto-refresh
if st.button("🔄 Refresh Page"):
    st.rerun()
