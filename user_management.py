import streamlit as st
import pandas as pd
import os
import pickle
import cv2
import numpy as np
from datetime import datetime
import json

def load_user_database():
    """Load user information database"""
    if os.path.exists('data/user_database.json'):
        with open('data/user_database.json', 'r') as f:
            return json.load(f)
    return {}

def save_user_database(db):
    """Save user information database"""
    with open('data/user_database.json', 'w') as f:
        json.dump(db, f, indent=4)

def main():
    st.set_page_config(page_title="👥 User Management System", layout="wide")
    st.title("👥 Face Recognition User Management")
    st.markdown("---")
    
    # Load current users
    user_db = load_user_database()
    
    # Load face recognition data
    try:
        with open('data/names.pkl', 'rb') as f:
            names = pickle.load(f)
        with open('data/faces_data.pkl', 'rb') as f:
            faces = pickle.load(f)
        
        current_users = list(set(names))
    except:
        current_users = []
        st.error("Could not load face recognition data!")
    
    # Sidebar navigation
    st.sidebar.header("🔧 Management Options")
    action = st.sidebar.selectbox(
        "Choose Action",
        ["View Users", "Add New User", "User Details", "Remove User", "Backup Data"]
    )
    
    if action == "View Users":
        st.header("📋 Current Users")
        
        if current_users:
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("👤 Registered Users")
                for i, user in enumerate(current_users, 1):
                    user_info = user_db.get(user, {})
                    role = user_info.get('role', 'Student')
                    st.write(f"{i}. **{user}** - {role}")
            
            with col2:
                st.subheader("📊 Statistics")
                st.metric("Total Users", len(current_users))
                st.metric("Face Samples", len(names))
                
                # Show user roles
                roles = [user_db.get(user, {}).get('role', 'Student') for user in current_users]
                role_counts = pd.Series(roles).value_counts()
                st.write("**Roles Distribution:**")
                for role, count in role_counts.items():
                    st.write(f"- {role}: {count}")
        else:
            st.warning("No users found in the system!")
    
    elif action == "Add New User":
        st.header("➕ Add New User")
        
        with st.form("add_user_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                name = st.text_input("👤 Full Name *")
                employee_id = st.text_input("🆔 Employee/Student ID")
                role = st.selectbox("👔 Role", ["Student", "Teacher", "Staff", "Admin"])
            
            with col2:
                department = st.text_input("🏢 Department")
                email = st.text_input("📧 Email")
                phone = st.text_input("📱 Phone Number")
            
            notes = st.text_area("📝 Notes")
            
            submitted = st.form_submit_button("💾 Save User Info")
            
            if submitted and name:
                # Save user info
                user_db[name] = {
                    'employee_id': employee_id,
                    'role': role,
                    'department': department,
                    'email': email,
                    'phone': phone,
                    'notes': notes,
                    'created_date': datetime.now().isoformat(),
                    'face_trained': name in current_users
                }
                save_user_database(user_db)
                st.success(f"✅ User {name} information saved!")
                
                if name not in current_users:
                    st.info("ℹ️ To complete registration, run face training:")
                    st.code("python addFaces.py")
    
    elif action == "User Details":
        st.header("👤 User Details")
        
        if current_users:
            selected_user = st.selectbox("Select User", current_users)
            
            if selected_user:
                user_info = user_db.get(selected_user, {})
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("📋 Basic Information")
                    st.write(f"**Name:** {selected_user}")
                    st.write(f"**Employee ID:** {user_info.get('employee_id', 'N/A')}")
                    st.write(f"**Role:** {user_info.get('role', 'Student')}")
                    st.write(f"**Department:** {user_info.get('department', 'N/A')}")
                
                with col2:
                    st.subheader("📞 Contact Information")
                    st.write(f"**Email:** {user_info.get('email', 'N/A')}")
                    st.write(f"**Phone:** {user_info.get('phone', 'N/A')}")
                    st.write(f"**Created:** {user_info.get('created_date', 'N/A')[:10] if user_info.get('created_date') else 'N/A'}")
                
                if user_info.get('notes'):
                    st.subheader("📝 Notes")
                    st.write(user_info['notes'])
                
                # Face recognition stats
                user_face_count = names.count(selected_user) if selected_user in names else 0
                st.subheader("🤖 Face Recognition Stats")
                st.metric("Face Samples Trained", user_face_count)
                
                if user_face_count > 0:
                    st.success("✅ Face recognition trained")
                else:
                    st.warning("⚠️ Face recognition not trained")
    
    elif action == "Remove User":
        st.header("🗑️ Remove User")
        st.warning("⚠️ This action will remove user from face recognition data!")
        
        if current_users:
            user_to_remove = st.selectbox("Select User to Remove", current_users)
            
            if st.button("❌ Remove User", type="primary"):
                st.error("🚧 Feature under development - Manual removal required")
                st.info("To manually remove a user, you'll need to retrain the system without that person's data.")
    
    elif action == "Backup Data":
        st.header("💾 Backup & Export")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📁 Create Backup")
            if st.button("🔒 Backup All Data"):
                backup_dir = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                os.makedirs(backup_dir, exist_ok=True)
                
                # Copy important files
                import shutil
                try:
                    shutil.copy('data/faces_data.pkl', backup_dir)
                    shutil.copy('data/names.pkl', backup_dir)
                    if os.path.exists('data/user_database.json'):
                        shutil.copy('data/user_database.json', backup_dir)
                    
                    st.success(f"✅ Backup created in {backup_dir}/")
                except Exception as e:
                    st.error(f"❌ Backup failed: {e}")
        
        with col2:
            st.subheader("📊 Export User Database")
            if user_db:
                user_df = pd.DataFrame.from_dict(user_db, orient='index')
                csv = user_df.to_csv()
                
                st.download_button(
                    label="📥 Download User Database (CSV)",
                    data=csv,
                    file_name=f"user_database_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                )

if __name__ == "__main__":
    main()
