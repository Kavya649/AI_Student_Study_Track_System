import streamlit as st
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

DATA_FILE = "Study_Track_AI_Project.csv"
LOG_FILE = "student_logs.csv"

# -------------------------
# Auth Check
# -------------------------
if not st.session_state.get("logged_in"):
    st.warning("Please log in to access this page.")
    st.stop()

# -------------------------
# Load Data
# -------------------------
dataset = pd.read_csv(DATA_FILE)

try:
    logs = pd.read_csv(LOG_FILE)
except:
    logs = pd.DataFrame(columns=[
        "Student_ID", "Date", "Study_Duration", "Subject", "Distractions", "Quiz_Score"
    ])
    logs.to_csv(LOG_FILE, index=False)  # ← fix: save empty df on first run

# -------------------------
# Header
# -------------------------
st.markdown("""
<div style="background:#8b6bdc;padding:20px;border-radius:10px;color:white;text-align:center;">
<h2>AI Student Study Tracking System</h2>
</div>
""", unsafe_allow_html=True)

st.subheader("⚙️ Admin Dashboard")

# -------------------------
# Dataset Management
# -------------------------
st.markdown("### 📁 Dataset Management")

file = st.file_uploader("Upload new CSV dataset", type="csv")

if file:
    dataset = pd.read_csv(file)
    dataset.to_csv(DATA_FILE, index=False)
    st.success("✅ Dataset updated successfully!")
    st.rerun()

# -------------------------
# System Metrics
# -------------------------
st.markdown("### 📊 System Metrics")

col1, col2 = st.columns(2)
col3, col4 = st.columns(2)

with col1:
    st.markdown(f"""
    <div style="padding:20px;border-radius:10px;background:#e3f2fd;text-align:center;">
    <h4>👥 Active Students</h4>
    <h2 style="color:#1976d2">{logs["Student_ID"].nunique()}</h2>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div style="padding:20px;border-radius:10px;background:#e8f5e8;text-align:center;">
    <h4>📝 Study Sessions</h4>
    <h2 style="color:#2e7d32">{len(logs)}</h2>
    </div>
    """, unsafe_allow_html=True)

avg_score = round(logs["Quiz_Score"].mean(), 2) if len(logs) > 0 else 0

with col3:
    st.markdown(f"""
    <div style="padding:20px;border-radius:10px;background:#fff3e0;text-align:center;">
    <h4>📈 Avg Quiz Score</h4>
    <h2 style="color:#f57c00">{avg_score}%</h2>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div style="padding:20px;border-radius:10px;background:#f3e5f5;text-align:center;">
    <h4>📊 Dataset Size</h4>
    <h2 style="color:#7b1fa2">{len(dataset)}</h2>
    </div>
    """, unsafe_allow_html=True)

# -------------------------
# Retrain Buttons
# -------------------------
st.markdown("### 🔄 Model Retraining")

col1, col2 = st.columns(2)

with col1:
    if st.button("🔄 Quick Retrain", type="primary"):
        if len(logs) > 0:
            agg = logs.groupby("Student_ID").agg({
                "Study_Duration": "mean",
                "Quiz_Score": "mean"
            }).reset_index()

            scaler = StandardScaler()
            X = scaler.fit_transform(agg[["Study_Duration", "Quiz_Score"]])

            kmeans = KMeans(n_clusters=min(3, len(agg)), n_init=10, random_state=42)
            agg["Cluster"] = kmeans.fit_predict(X)

            dataset = dataset.merge(
                agg[["Student_ID", "Cluster"]],
                on="Student_ID",
                how="left",
                suffixes=("", "_new")
            )

            dataset["Cluster"] = dataset["Cluster_new"].combine_first(dataset["Cluster"])
            dataset.drop(columns=["Cluster_new"], inplace=True, errors='ignore')
            dataset.to_csv(DATA_FILE, index=False)
            st.success("✅ Quick retraining completed!")
            st.rerun()
        else:
            st.warning("No logs available for quick retrain!")

with col2:
    if st.button("🔄 Full Retrain"):
        features = dataset[[
            "Study_Hours_per_Week",
            "Attendance_Percentage",
            "Assignments_Completed",
            "Mock_Test_Score",
            "Final_Exam_Score"
        ]].fillna(0)

        scaler = StandardScaler()
        X = scaler.fit_transform(features)

        kmeans = KMeans(n_clusters=min(5, len(dataset)), n_init=10, random_state=42)
        dataset["Cluster"] = kmeans.fit_predict(X)
        dataset.to_csv(DATA_FILE, index=False)
        st.success("✅ Full retraining completed!")
        st.rerun()
