import streamlit as st
import pandas as pd
import time
import os
import pickle
import numpy as np
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go

# Set page configuration
st.set_page_config(
    page_title="Face Recognition Attendance System", 
    page_icon="🎯", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'Dashboard'

# Sidebar Navigation
st.sidebar.title("🎯 Navigation")
st.sidebar.markdown("---")

# Navigation buttons
if st.sidebar.button("📊 Dashboard", use_container_width=True):
    st.session_state.current_page = 'Dashboard'
    
if st.sidebar.button("👥 User Management", use_container_width=True):
    st.session_state.current_page = 'User Management'
    
if st.sidebar.button("📈 Analytics", use_container_width=True):
    st.session_state.current_page = 'Analytics'
    
if st.sidebar.button("⚙️ Settings", use_container_width=True):
    st.session_state.current_page = 'Settings'

# Sidebar System Info
st.sidebar.markdown("---")
st.sidebar.markdown("### 🖥️ System Status")

# Load system data with error handling for cloud deployment
try:
    if os.path.exists('data/names.pkl') and os.path.exists('data/faces_data.pkl'):
        with open('data/names.pkl', 'rb') as f:
            all_names = pickle.load(f)
        with open('data/faces_data.pkl', 'rb') as f:
            all_faces = pickle.load(f)
        trained_people = list(set(all_names))
    else:
        # Default data for cloud deployment demo
        all_names = ['Akshita', 'Anshita', 'Papa', 'Mumma'] * 100  # 400 samples
        all_faces = np.random.rand(400, 50, 50)  # Dummy face data
        trained_people = ['Akshita', 'Anshita', 'Papa', 'Mumma']
    st.sidebar.success(f"✅ System Active")
    st.sidebar.info(f"👥 {len(trained_people)} people trained")
    st.sidebar.info(f"📊 {len(all_faces)} face samples")
except:
    st.sidebar.error("❌ No training data")
    trained_people = []

# Main Content Area
if st.session_state.current_page == 'Dashboard':
    st.title("📊 Face Recognition Attendance Dashboard")
    st.markdown("---")
    
    # Get current date
    ts = time.time()
    date = datetime.fromtimestamp(ts).strftime("%d-%m-%y")
    timestamp = datetime.fromtimestamp(ts).strftime("%H:%M-%S")
    
    # Today's attendance section
    st.markdown("### 📅 Today's Attendance")
    attendance_file = f"Attendance/Attendance_{date}.csv"
    
    col1, col2, col3, col4 = st.columns(4)
    
    if os.path.exists(attendance_file):
        try:
            df = pd.read_csv(attendance_file)
            if not df.empty:
                with col1:
                    st.metric("📋 Total Records", len(df))
                with col2:
                    if 'NAME' in df.columns:
                        unique_people_today = df['NAME'].nunique()
                        st.metric("👥 Unique People", unique_people_today)
                with col3:
                    st.metric("📅 Date", date)
                with col4:
                    st.metric("🕐 Last Updated", timestamp)
                
                st.dataframe(df.style.highlight_max(axis=0), use_container_width=True)
            else:
                st.info("📝 No attendance recorded today")
        except Exception as e:
            st.error(f"Error reading attendance: {str(e)}")
    else:
        st.info(f"📋 No attendance file found for today ({date})")
        
    # System Information
    st.markdown("### 🖥️ System Information")
    if trained_people:
        st.success(f"**Trained People ({len(trained_people)})**: {', '.join(sorted(trained_people))}")
    else:
        st.warning("No people trained in the system")
    
    # Quick Actions
    st.markdown("### ⚡ Quick Actions")
    action_col1, action_col2, action_col3 = st.columns(3)
    
    with action_col1:
        if st.button("🎥 Start Face Recognition", use_container_width=True):
            st.info("💡 Run this command in terminal: `python test.py`")
            
    with action_col2:
        if st.button("👤 Add New Person", use_container_width=True):
            st.info("💡 Run this command in terminal: `python addFaces.py`")
            
    with action_col3:
        if st.button("🔄 Refresh Data", use_container_width=True):
            st.rerun()

elif st.session_state.current_page == 'User Management':
    st.title("👥 User Management")
    st.markdown("---")
    
    # Display current users
    if trained_people:
        st.markdown("### 👨‍👩‍👧‍👦 Registered Users")
        
        # Create user cards
        cols = st.columns(3)
        for i, person in enumerate(sorted(trained_people)):
            with cols[i % 3]:
                with st.container():
                    st.markdown(f"""
                    <div style="padding: 1rem; border: 1px solid #ddd; border-radius: 0.5rem; margin: 0.5rem 0;">
                        <h4>👤 {person}</h4>
                        <p>Status: ✅ Active</p>
                    </div>
                    """, unsafe_allow_html=True)
        
        # User actions
        st.markdown("### ⚙️ User Actions")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### ➕ Add New User")
            new_user_name = st.text_input("Enter new user name:")
            if st.button("Add User", use_container_width=True):
                if new_user_name:
                    st.info(f"💡 To add '{new_user_name}', run: `python addFaces.py`")
                    st.info("Then enter the name when prompted")
                else:
                    st.warning("Please enter a name")
        
        with col2:
            st.markdown("#### 🗑️ Remove User")
            if st.button("Reset All Users", use_container_width=True):
                st.warning("⚠️ This will remove all trained faces!")
                if st.button("Confirm Reset", use_container_width=True):
                    st.info("💡 Run the fresh start script to reset all data")
    else:
        st.warning("No users registered in the system")
        st.markdown("### 🚀 Get Started")
        if st.button("Add First User", use_container_width=True):
            st.info("💡 Run this command: `python addFaces.py`")

elif st.session_state.current_page == 'Analytics':
    st.title("📈 Analytics & Reports")
    st.markdown("---")
    
    # Load all attendance files with error handling
    attendance_files = []
    if os.path.exists("Attendance/"):
        attendance_files = [f for f in os.listdir("Attendance/") if f.endswith('.csv')]
    
    if attendance_files:
        # Combine all attendance data
        all_data = []
        for file in attendance_files:
            try:
                df = pd.read_csv(f"Attendance/{file}")
                if not df.empty and 'NAME' in df.columns:
                    # Extract date from filename
                    date_str = file.replace('Attendance_', '').replace('.csv', '')
                    df['DATE'] = date_str
                    all_data.append(df)
            except:
                continue
        
        if all_data:
            combined_df = pd.concat(all_data, ignore_index=True)
            
            # Analytics
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### 👥 Attendance by Person")
                person_counts = combined_df['NAME'].value_counts()
                fig_bar = px.bar(
                    x=person_counts.index,
                    y=person_counts.values,
                    labels={'x': 'Person', 'y': 'Attendance Count'},
                    title="Total Attendance by Person"
                )
                st.plotly_chart(fig_bar, use_container_width=True)
            
            with col2:
                st.markdown("#### 📅 Daily Attendance")
                daily_counts = combined_df['DATE'].value_counts().sort_index()
                fig_line = px.line(
                    x=daily_counts.index,
                    y=daily_counts.values,
                    labels={'x': 'Date', 'y': 'Total Attendance'},
                    title="Daily Attendance Trend"
                )
                st.plotly_chart(fig_line, use_container_width=True)
            
            # Summary statistics
            st.markdown("### 📊 Summary Statistics")
            summary_col1, summary_col2, summary_col3, summary_col4 = st.columns(4)
            
            with summary_col1:
                st.metric("📋 Total Records", len(combined_df))
            with summary_col2:
                st.metric("👥 Unique People", combined_df['NAME'].nunique())
            with summary_col3:
                st.metric("📅 Days with Data", combined_df['DATE'].nunique())
            with summary_col4:
                avg_daily = len(combined_df) / combined_df['DATE'].nunique()
                st.metric("📈 Avg Daily Attendance", f"{avg_daily:.1f}")
            
            # Raw data table
            st.markdown("### 📄 All Attendance Records")
            st.dataframe(combined_df, use_container_width=True)
        else:
            st.info("No valid attendance data found")
    else:
        st.info("No attendance files found")

elif st.session_state.current_page == 'Settings':
    st.title("⚙️ System Settings")
    st.markdown("---")
    
    # System Information
    st.markdown("### 🖥️ System Information")
    
    info_col1, info_col2 = st.columns(2)
    
    with info_col1:
        st.markdown("#### 📊 Training Data")
        if trained_people:
            st.success(f"✅ {len(trained_people)} people trained")
            st.info(f"📈 {len(all_faces)} total face samples")
            st.info(f"🎯 Average samples per person: {len(all_faces)//len(trained_people) if trained_people else 0}")
        else:
            st.warning("❌ No training data found")
    
    with info_col2:
        st.markdown("#### 📁 Data Files")
        if os.path.exists("data/"):
            data_files = os.listdir("data/")
            for file in data_files:
                if file.endswith('.pkl'):
                    st.info(f"📄 {file}")
                elif file.endswith('.xml'):
                    st.info(f"🤖 {file}")
        else:
            st.warning("Data directory not found")
    
    # System Actions
    st.markdown("### 🔧 System Actions")
    
    action_col1, action_col2 = st.columns(2)
    
    with action_col1:
        st.markdown("#### 🔄 Data Management")
        if st.button("Backup Current Data", use_container_width=True):
            st.info("💡 Data backup functionality would go here")
        
        if st.button("Export Attendance Data", use_container_width=True):
            st.info("💡 Export functionality would go here")
    
    with action_col2:
        st.markdown("#### 🗑️ Reset Options")
        if st.button("Reset Training Data", use_container_width=True):
            st.warning("⚠️ This will delete all face training data!")
        
        if st.button("Clear Attendance Records", use_container_width=True):
            st.warning("⚠️ This will delete all attendance records!")

# Footer
st.markdown("---")
st.markdown("### 💡 Quick Commands")
st.code("""
# Start face recognition
python test.py

# Add new person
python addFaces.py

# View this dashboard
streamlit run unified_dashboard.py
""")

st.markdown("---")
st.markdown("**🎯 Face Recognition Attendance System** | Built with Streamlit & OpenCV")
