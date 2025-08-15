import streamlit as st 
import pandas as pd
import time
import os
from datetime import datetime

# Set page configuration
st.set_page_config(page_title="Face Recognition Attendance System", page_icon="📊", layout="wide")

# Title and header
st.title("🎯 Face Recognition Attendance System")
st.markdown("---")

# Get current date
ts = time.time()
date = datetime.fromtimestamp(ts).strftime("%d-%m-%y")
timestamp = datetime.fromtimestamp(ts).strftime("%H:%M-%S")

# File path for today's attendance
attendance_file = f"Attendance/Attendance_{date}.csv"

# Check if today's attendance file exists
if os.path.exists(attendance_file):
    try:
        df = pd.read_csv(attendance_file)
        
        if not df.empty:
            st.success(f"📅 Attendance for {date}")
            st.dataframe(df.style.highlight_max(axis=0), use_container_width=True)
            
            # Show some statistics
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Records", len(df))
            with col2:
                if 'NAME' in df.columns:
                    unique_people = df['NAME'].nunique()
                    st.metric("Unique People", unique_people)
            with col3:
                st.metric("Date", date)
            
            # Show trained people info
            st.markdown("### 👥 System Information")
            try:
                import pickle
                with open('data/names.pkl', 'rb') as f:
                    all_names = pickle.load(f)
                trained_people = list(set(all_names))
                st.info(f"**Trained People ({len(trained_people)})**: {', '.join(sorted(trained_people))}")
            except:
                st.warning("Could not load trained people information")
                
        else:
            st.warning("📝 Attendance file exists but is empty")
            
    except Exception as e:
        st.error(f"Error reading attendance file: {str(e)}")
        
else:
    st.info(f"📋 No attendance records found for today ({date})")
    st.write("To start taking attendance:")
    st.write("1. Run the face recognition system: `python test.py`")
    st.write("2. Press 'o' when a face is detected to mark attendance")
    
    # Show available attendance files
    st.markdown("### 📁 Available Attendance Files:")
    attendance_files = [f for f in os.listdir("Attendance/") if f.endswith('.csv')]
    
    if attendance_files:
        selected_file = st.selectbox("View previous attendance:", attendance_files)
        if selected_file:
            try:
                prev_df = pd.read_csv(f"Attendance/{selected_file}")
                st.dataframe(prev_df.style.highlight_max(axis=0), use_container_width=True)
            except Exception as e:
                st.error(f"Error reading {selected_file}: {str(e)}")
    else:
        st.write("No previous attendance files found.")

# Refresh button
if st.button("🔄 Refresh Data"):
    st.rerun()