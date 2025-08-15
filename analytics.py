import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import os
import glob

st.set_page_config(page_title="📊 Advanced Attendance Analytics", layout="wide")

def load_all_attendance_data():
    """Load all attendance files and combine them"""
    all_files = glob.glob("Attendance/Attendance_*.csv")
    all_data = []
    
    for file in all_files:
        try:
            df = pd.read_csv(file)
            if not df.empty and 'NAME' in df.columns:
                # Extract date from filename
                date_str = file.split('_')[1].replace('.csv', '')
                df['DATE'] = date_str
                df['FULL_DATE'] = pd.to_datetime(date_str, format='%d-%m-%y')
                all_data.append(df)
        except:
            continue
    
    if all_data:
        return pd.concat(all_data, ignore_index=True)
    return pd.DataFrame()

def main():
    st.title("📊 Advanced Face Recognition Attendance Analytics")
    st.markdown("---")
    
    # Load data
    df_all = load_all_attendance_data()
    
    if df_all.empty:
        st.warning("No attendance data found!")
        return
    
    # Sidebar filters
    st.sidebar.header("🔍 Filters")
    
    # Date range filter
    min_date = df_all['FULL_DATE'].min()
    max_date = df_all['FULL_DATE'].max()
    
    date_range = st.sidebar.date_input(
        "Select Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )
    
    # Person filter
    all_people = df_all['NAME'].unique()
    selected_people = st.sidebar.multiselect(
        "Select People",
        options=all_people,
        default=all_people
    )
    
    # Filter data
    if len(date_range) == 2:
        mask = (df_all['FULL_DATE'] >= pd.Timestamp(date_range[0])) & \
               (df_all['FULL_DATE'] <= pd.Timestamp(date_range[1])) & \
               (df_all['NAME'].isin(selected_people))
        filtered_df = df_all[mask]
    else:
        filtered_df = df_all[df_all['NAME'].isin(selected_people)]
    
    # Main dashboard
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📊 Total Records", len(filtered_df))
    with col2:
        st.metric("👥 Unique People", filtered_df['NAME'].nunique())
    with col3:
        st.metric("📅 Days Covered", filtered_df['DATE'].nunique())
    with col4:
        if not filtered_df.empty:
            avg_daily = len(filtered_df) / max(1, filtered_df['DATE'].nunique())
            st.metric("📈 Avg Daily Records", f"{avg_daily:.1f}")
    
    st.markdown("---")
    
    # Charts section
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Attendance by Person")
        if not filtered_df.empty:
            person_counts = filtered_df['NAME'].value_counts()
            fig_pie = px.pie(
                values=person_counts.values,
                names=person_counts.index,
                title="Distribution of Attendance Records"
            )
            st.plotly_chart(fig_pie, use_container_width=True)
    
    with col2:
        st.subheader("📈 Daily Attendance Trend")
        if not filtered_df.empty:
            daily_counts = filtered_df.groupby('FULL_DATE').size().reset_index()
            daily_counts.columns = ['Date', 'Count']
            
            fig_line = px.line(
                daily_counts,
                x='Date',
                y='Count',
                title="Daily Attendance Count",
                markers=True
            )
            st.plotly_chart(fig_line, use_container_width=True)
    
    # Detailed table
    st.subheader("📋 Detailed Records")
    if not filtered_df.empty:
        # Sort by date and time
        display_df = filtered_df[['NAME', 'TIME', 'DATE']].sort_values(['DATE', 'TIME'], ascending=[False, False])
        st.dataframe(display_df, use_container_width=True)
    
    # Export options
    st.markdown("---")
    st.subheader("💾 Export Data")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📥 Download as CSV"):
            csv = filtered_df.to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name=f"attendance_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
    
    with col2:
        if st.button("📊 Generate Report"):
            st.balloons()
            st.success("Report generated successfully!")

if __name__ == "__main__":
    main()
