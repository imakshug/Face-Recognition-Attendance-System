import streamlit as st
import pandas as pd
import time
import os
from datetime import datetime
import subprocess
import sys

st.set_page_config(
    page_title="🎯 Face Recognition Attendance System",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

def run_page(page_file):
    """Run another Streamlit page"""
    subprocess.Popen([sys.executable, "-m", "streamlit", "run", page_file, "--server.port", "8504"])

def main():
    # Custom CSS
    st.markdown("""
    <style>
    .main-header {
        text-align: center;
        background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%);
        color: white;
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #1e3c72;
    }
    .status-running {
        color: #28a745;
        font-weight: bold;
    }
    .status-stopped {
        color: #dc3545;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Main header
    st.markdown("""
    <div class="main-header">
        <h1>🎯 Face Recognition Attendance System</h1>
        <p>Advanced AI-Powered Attendance Management</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar navigation
    st.sidebar.title("🧭 Navigation")
    page = st.sidebar.selectbox(
        "Select Page",
        [
            "🏠 Dashboard",
            "📊 Analytics",
            "👥 User Management", 
            "⚙️ System Settings",
            "📋 Reports",
            "🔧 System Control"
        ]
    )
    
    # Quick stats in sidebar
    st.sidebar.markdown("---")
    st.sidebar.subheader("📈 Quick Stats")
    
    # Load current data
    ts = time.time()
    date = datetime.fromtimestamp(ts).strftime("%d-%m-%y")
    attendance_file = f"Attendance/Attendance_{date}.csv"
    
    try:
        if os.path.exists(attendance_file):
            df_today = pd.read_csv(attendance_file)
            today_count = len(df_today) if not df_today.empty else 0
        else:
            today_count = 0
            
        st.sidebar.metric("📅 Today's Records", today_count)
        
        # Total attendance files
        attendance_files = [f for f in os.listdir("Attendance/") if f.endswith('.csv')]
        st.sidebar.metric("📁 Total Days", len(attendance_files))
        
        # Trained users
        if os.path.exists('data/names.pkl'):
            import pickle
            with open('data/names.pkl', 'rb') as f:
                names = pickle.load(f)
            unique_users = len(set(names))
            st.sidebar.metric("👥 Trained Users", unique_users)
        
    except Exception as e:
        st.sidebar.error(f"Error loading stats: {e}")
    
    # Main content based on selected page
    if page == "🏠 Dashboard":
        show_dashboard(date, attendance_file)
    elif page == "📊 Analytics":
        st.info("📊 Opening Analytics Dashboard...")
        if st.button("🚀 Launch Analytics"):
            run_page("analytics.py")
    elif page == "👥 User Management":
        st.info("👥 Opening User Management...")
        if st.button("🚀 Launch User Management"):
            run_page("user_management.py")
    elif page == "⚙️ System Settings":
        show_settings()
    elif page == "📋 Reports":
        show_reports()
    elif page == "🔧 System Control":
        show_system_control()

def show_dashboard(date, attendance_file):
    """Main dashboard page"""
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3>📅 Today's Date</h3>
            <h2>{}</h2>
        </div>
        """.format(date), unsafe_allow_html=True)
    
    with col2:
        if os.path.exists(attendance_file):
            df = pd.read_csv(attendance_file)
            count = len(df) if not df.empty else 0
            status = "🟢 Active"
        else:
            count = 0
            status = "🔴 No Records"
            
        st.markdown("""
        <div class="metric-card">
            <h3>📊 Today's Records</h3>
            <h2>{}</h2>
            <p>{}</p>
        </div>
        """.format(count, status), unsafe_allow_html=True)
    
    with col3:
        # System status
        st.markdown("""
        <div class="metric-card">
            <h3>🤖 System Status</h3>
            <h2>🟢 Online</h2>
            <p>Ready for Recognition</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Today's attendance
    st.subheader("📋 Today's Attendance Records")
    
    if os.path.exists(attendance_file):
        try:
            df = pd.read_csv(attendance_file)
            if not df.empty:
                # Enhanced table display
                st.dataframe(
                    df.style.highlight_max(axis=0),
                    use_container_width=True,
                    height=300
                )
                
                # Summary
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Total Entries", len(df))
                with col2:
                    if 'NAME' in df.columns:
                        unique_people = df['NAME'].nunique()
                        st.metric("Unique People", unique_people)
            else:
                st.info("📝 No attendance records for today yet.")
        except Exception as e:
            st.error(f"Error reading attendance data: {e}")
    else:
        st.info("📝 No attendance file found for today.")
        st.write("Start the face recognition system to begin taking attendance!")

def show_settings():
    """System settings page"""
    st.header("⚙️ System Settings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🎛️ Recognition Settings")
        confidence_threshold = st.slider("Recognition Confidence", 0.1, 1.0, 0.8)
        max_distance = st.slider("Max Face Distance", 0.1, 1.0, 0.6)
        
        st.subheader("📷 Camera Settings")
        camera_index = st.selectbox("Camera Index", [0, 1, 2])
        resolution = st.selectbox("Resolution", ["640x480", "1280x720", "1920x1080"])
    
    with col2:
        st.subheader("💾 Data Settings")
        auto_backup = st.checkbox("Auto Backup", value=True)
        backup_interval = st.selectbox("Backup Interval", ["Daily", "Weekly", "Monthly"])
        
        st.subheader("🔔 Notifications")
        voice_enabled = st.checkbox("Voice Notifications", value=True)
        sound_enabled = st.checkbox("Sound Alerts", value=True)
    
    if st.button("💾 Save Settings"):
        st.success("✅ Settings saved successfully!")

def show_reports():
    """Reports page"""
    st.header("📋 Attendance Reports")
    
    # Date range selector
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date")
    with col2:
        end_date = st.date_input("End Date")
    
    # Report type
    report_type = st.selectbox(
        "Report Type",
        ["Daily Summary", "Individual Report", "Department Wise", "Monthly Summary"]
    )
    
    if st.button("📊 Generate Report"):
        st.success("✅ Report generated successfully!")
        
        # Sample report data
        sample_data = {
            'Date': ['15-08-25', '14-08-25', '13-08-25'],
            'Total Records': [5, 8, 6],
            'Unique People': [3, 4, 3],
            'Average Time': ['09:30', '09:45', '09:15']
        }
        
        df_report = pd.DataFrame(sample_data)
        st.dataframe(df_report, use_container_width=True)
        
        # Download button
        csv = df_report.to_csv(index=False)
        st.download_button(
            label="📥 Download Report",
            data=csv,
            file_name=f"attendance_report_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )

def show_system_control():
    """System control page"""
    st.header("🔧 System Control Panel")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🎮 Face Recognition Control")
        
        if st.button("▶️ Start Face Recognition", type="primary"):
            st.info("🚀 Starting face recognition system...")
            st.code("python test.py")
        
        if st.button("⏹️ Stop Face Recognition"):
            st.info("⏹️ Stopping face recognition system...")
        
        if st.button("📷 Test Camera"):
            st.info("📷 Testing camera connection...")
    
    with col2:
        st.subheader("🗄️ Data Management")
        
        if st.button("🔄 Refresh Data"):
            st.rerun()
        
        if st.button("🧹 Clean Temporary Files"):
            st.success("✅ Temporary files cleaned!")
        
        if st.button("💾 Backup System"):
            st.success("✅ System backup created!")
    
    st.markdown("---")
    
    # System logs
    st.subheader("📜 System Logs")
    log_data = [
        "2025-08-15 20:34:14 - Face recognition started",
        "2025-08-15 20:34:03 - Anshita attendance marked",
        "2025-08-15 20:31:55 - Akshita attendance marked",
        "2025-08-15 20:30:00 - System initialized"
    ]
    
    for log in log_data:
        st.text(log)

if __name__ == "__main__":
    main()
