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
from PIL import Image
import tempfile

# Page configuration
st.set_page_config(
    page_title="📷 Web Dashboard Attendance",
    page_icon="📋",
    layout="wide"
)

st.title("📋 Face Recognition Attendance Dashboard")
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
        st.error("❌ Face recognition data not found. Please train the model first using addFaces.py")
        return None, None

# Initialize KNN model
@st.cache_resource
def load_models():
    names, faces = load_face_data()
    if names is not None and faces is not None:
        knn = KNeighborsClassifier(n_neighbors=5)
        knn.fit(faces, names)
        face_detector = cv2.CascadeClassifier('data/haarcascade_frontalface_default.xml')
        return knn, face_detector, names
    return None, None, None

# Load models
knn_model, face_detector, trained_names = load_models()

if knn_model is None:
    st.error("❌ Could not load face recognition models. Please train the system first.")
    st.stop()

# Sidebar
st.sidebar.header("🎯 Attendance Controls")

# Method selection
attendance_method = st.sidebar.radio(
    "Choose attendance method:",
    ["📷 Camera Capture", "✏️ Manual Entry", "📊 View Records"]
)

if attendance_method == "📷 Camera Capture":
    st.header("📷 Camera-Based Attendance")
    
    # Camera controls
    col1, col2 = st.columns([3, 1])
    
    with col1:
        camera_enabled = st.checkbox("🔴 Enable Camera", value=False)
    
    with col2:
        confidence_threshold = st.slider("Confidence", 0.5, 1.0, 0.8, 0.05)
    
    if camera_enabled:
        # Camera capture
        camera_placeholder = st.empty()
        
        # Use OpenCV to capture from camera
        if st.button("📸 Take Photo for Attendance"):
            cap = cv2.VideoCapture(0)
            if cap.isOpened():
                ret, frame = cap.read()
                if ret:
                    # Process the frame
                    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    faces = face_detector.detectMultiScale(gray, 1.3, 5)
                    
                    recognized_persons = []
                    
                    for (x, y, w, h) in faces:
                        # Extract face
                        face_roi = frame[y:y+h, x:x+w]
                        resized_face = cv2.resize(face_roi, (50, 50)).flatten().reshape(1, -1)
                        
                        # Predict
                        prediction = knn_model.predict(resized_face)
                        probabilities = knn_model.predict_proba(resized_face)
                        confidence = np.max(probabilities)
                        
                        if confidence >= confidence_threshold:
                            name = prediction[0]
                            recognized_persons.append((name, confidence))
                            
                            # Draw rectangle and label
                            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                            cv2.putText(frame, f"{name} ({confidence:.2f})", 
                                      (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                        else:
                            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)
                            cv2.putText(frame, "Unknown", (x, y-10), 
                                      cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                    
                    # Display the processed frame
                    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    st.image(frame_rgb, caption="Captured Image with Recognition Results")
                    
                    # Show recognition results
                    if recognized_persons:
                        st.success(f"🎯 Recognized {len(recognized_persons)} person(s):")
                        for name, conf in recognized_persons:
                            col1, col2 = st.columns([3, 1])
                            with col1:
                                st.write(f"**{name}** (Confidence: {conf:.2f})")
                            with col2:
                                if st.button(f"✅ Mark {name}", key=f"mark_{name}"):
                                    # Save attendance
                                    ts = time.time()
                                    date = datetime.fromtimestamp(ts).strftime("%d-%m-%y")
                                    timestamp = datetime.fromtimestamp(ts).strftime("%H:%M-%S")
                                    
                                    attendance_file = f"Attendance/Attendance_{date}.csv"
                                    attendance_data = [name, timestamp]
                                    
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
                                        
                                        st.success(f"✅ Attendance marked for {name} at {timestamp}!")
                                        st.balloons()
                                        
                                    except Exception as e:
                                        st.error(f"❌ Error saving attendance: {str(e)}")
                    else:
                        st.warning("⚠️ No faces recognized with sufficient confidence. Try again with better lighting.")
                
                cap.release()
            else:
                st.error("❌ Could not access camera. Please check camera permissions.")
    
    else:
        st.info("📸 Click 'Enable Camera' to start camera-based attendance")

elif attendance_method == "✏️ Manual Entry":
    st.header("✏️ Manual Attendance Entry")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        available_names = list(set(trained_names))
        selected_name = st.selectbox("👤 Select Person", available_names)
    
    with col2:
        entry_date = st.date_input("📅 Date", datetime.now().date())
    
    with col3:
        entry_time = st.time_input("🕐 Time", datetime.now().time())
    
    if st.button("➕ Add Manual Attendance", type="primary"):
        # Format the data
        date_str = entry_date.strftime("%d-%m-%y")
        time_str = entry_time.strftime("%H:%M-%S")
        
        attendance_file = f"Attendance/Attendance_{date_str}.csv"
        attendance_data = [selected_name, time_str]
        
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
            
            st.success(f"✅ Manual attendance added for {selected_name} on {date_str} at {time_str}!")
            
        except Exception as e:
            st.error(f"❌ Error adding manual attendance: {str(e)}")

elif attendance_method == "📊 View Records":
    st.header("📊 Attendance Records")
    
    # Date selector
    view_date = st.date_input("📅 Select Date to View", datetime.now().date())
    date_str = view_date.strftime("%d-%m-%y")
    attendance_file = f"Attendance/Attendance_{date_str}.csv"
    
    if os.path.exists(attendance_file):
        try:
            df = pd.read_csv(attendance_file)
            if not df.empty:
                st.success(f"📋 Attendance for {date_str}")
                st.dataframe(df, use_container_width=True)
                
                # Statistics
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("📊 Total Records", len(df))
                with col2:
                    if 'NAME' in df.columns:
                        unique_people = df['NAME'].nunique()
                        st.metric("👥 Unique People", unique_people)
                with col3:
                    st.metric("📅 Date", date_str)
                with col4:
                    if 'TIME' in df.columns and len(df) > 0:
                        first_time = df['TIME'].iloc[0]
                        st.metric("🕐 First Entry", first_time)
                
                # Download option
                csv_data = df.to_csv(index=False)
                st.download_button(
                    label="📥 Download CSV",
                    data=csv_data,
                    file_name=f"Attendance_{date_str}.csv",
                    mime="text/csv"
                )
                
            else:
                st.warning(f"📝 Attendance file for {date_str} exists but is empty")
        except Exception as e:
            st.error(f"❌ Error reading attendance file: {str(e)}")
    else:
        st.info(f"📋 No attendance records found for {date_str}")
        
        # Show available files
        st.subheader("📁 Available Attendance Files")
        try:
            attendance_files = [f for f in os.listdir("Attendance/") if f.endswith('.csv')]
            if attendance_files:
                selected_file = st.selectbox("Select a file to view:", attendance_files)
                if selected_file:
                    file_df = pd.read_csv(f"Attendance/{selected_file}")
                    st.dataframe(file_df, use_container_width=True)
            else:
                st.info("No attendance files found")
        except Exception as e:
            st.error(f"Error accessing attendance files: {str(e)}")

# System Information Sidebar
st.sidebar.markdown("---")
st.sidebar.subheader("🔧 System Info")
st.sidebar.info(f"👥 Trained People: {len(set(trained_names))}")
st.sidebar.info(f"📊 Training Samples: {len(trained_names)}")

# Current trained people
with st.sidebar.expander("👥 Trained People"):
    for name in set(trained_names):
        st.sidebar.write(f"• {name}")

# Instructions
with st.sidebar.expander("📖 Instructions"):
    st.sidebar.markdown("""
    **Camera Attendance:**
    1. Enable camera
    2. Take photo
    3. Click mark attendance for recognized faces
    
    **Manual Entry:**
    1. Select person and time
    2. Click 'Add Manual Attendance'
    
    **View Records:**
    1. Select date
    2. View attendance data
    3. Download CSV if needed
    """)

# Auto-refresh option
if st.sidebar.button("🔄 Refresh Data"):
    st.cache_data.clear()
    st.rerun()
