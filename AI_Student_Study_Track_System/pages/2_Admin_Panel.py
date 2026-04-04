import streamlit as st
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import plotly.express as px
import plotly.graph_objects as go
import json

# -------------------------
# set_page_config at top
# -------------------------
st.set_page_config(layout="wide")

# -------------------------
# Styling
# -------------------------
st.markdown("""
<style>
.stApp {background-color:#f5f7fb;}

section[data-testid="stSidebar"]{
background-color:#ffffff;
border-right:1px solid #e5e7eb;
}

h1,h2,h3{color:#1f2937;}

.stButton>button{
background-color:#4f46e5;
color:white;
border-radius:8px;
border:none;
padding:10px 18px;
}

.stButton>button:hover{
background-color:#4338ca;
}

.card{
background-color:white;
padding:20px;
border-radius:12px;
border:1px solid #e5e7eb;
}
</style>
""", unsafe_allow_html=True)

st.title("⚙ Admin Panel")
st.markdown("This dashboard clusters student academic behavior using real dataset.")

# -------------------------
# Data Upload
# -------------------------
st.subheader("📁 Data Upload")

file = st.file_uploader("Upload CSV Dataset", type=["csv"])

if file:
    df = pd.read_csv(file)
    df.to_csv("Study_Track_AI_Project.csv", index=False)
    st.success("✅ Dataset updated successfully")

# -------------------------
# Load Dataset
# -------------------------
@st.cache_data
def load_data():
    return pd.read_csv("Study_Track_AI_Project.csv")

if "data" not in st.session_state:
    st.session_state.data = load_data()

data = st.session_state.data.copy()

# -------------------------
# Clustering
# -------------------------
st.subheader("🔢 KMeans Clusters")

n_clusters = st.number_input("Select number of clusters", 2, 10, 4)

features = data[[
    'Study_Hours_per_Week',
    'Attendance_Percentage',
    'Assignments_Completed',
    'Mock_Test_Score',
    'Final_Exam_Score'
]]

scaler = StandardScaler()
X_scaled = scaler.fit_transform(features)

kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
data['Cluster'] = kmeans.fit_predict(X_scaled)

# -------------------------
# Dynamic Cluster Labels
# -------------------------
cluster_summary = data.groupby('Cluster')['Final_Exam_Score'].mean()
sorted_clusters = cluster_summary.sort_values()

labels = [
    "Needs Improvement",
    "Low Engagement",
    "Average Learner",
    "Focused Studier",
    "Consistent Performer",
    "Good Performer",
    "High Achiever",
    "Top Performer",
    "Outstanding Student",
    "Elite Performer"
]

cluster_names = {}
for i, cluster_id in enumerate(sorted_clusters.index):
    cluster_names[cluster_id] = labels[i]

data['Cluster_Name'] = data['Cluster'].map(cluster_names)

# Save config
config = {"n_clusters": n_clusters, "cluster_labels": cluster_names}
with open("cluster_config.json", "w") as f:
    json.dump(config, f)

st.session_state.data = data

# -------------------------
# Model Retraining
# -------------------------
st.subheader("🔄 Model Retraining")

if st.button("Retrain Clustering Model"):
    st.session_state.data = load_data()
    data = st.session_state.data.copy()

    features = data[[
        'Study_Hours_per_Week',
        'Attendance_Percentage',
        'Assignments_Completed',
        'Mock_Test_Score',
        'Final_Exam_Score'
    ]]

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(features)

    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    data['Cluster'] = kmeans.fit_predict(X_scaled)

    cluster_summary = data.groupby('Cluster')['Final_Exam_Score'].mean()
    sorted_clusters = cluster_summary.sort_values()

    cluster_names = {}
    for i, cluster_id in enumerate(sorted_clusters.index):
        cluster_names[cluster_id] = labels[i]

    data['Cluster_Name'] = data['Cluster'].map(cluster_names)

    config = {"n_clusters": n_clusters, "cluster_labels": cluster_names}
    with open("cluster_config.json", "w") as f:
        json.dump(config, f)

    data.to_csv("Study_Track_AI_Project.csv", index=False)
    st.session_state.data = data
    st.success("✅ Model retrained successfully!")
    st.rerun()

# -------------------------
# Cluster Metrics
# -------------------------
cluster_metrics = data.groupby('Cluster_Name')[[
    'Study_Hours_per_Week',
    'Attendance_Percentage',
    'Assignments_Completed',
    'Mock_Test_Score',
    'Final_Exam_Score'
]].mean().reset_index()

# -------------------------
# Sample Data
# -------------------------
st.subheader("📋 Sample Student Data")
st.dataframe(data)

# -------------------------
# Scatter Plot
# -------------------------
st.subheader("📊 Student Behavior Clusters")

fig_scatter = px.scatter(
    data,
    x='Study_Hours_per_Week',
    y='Final_Exam_Score',
    color='Cluster_Name',
    hover_data=['Student_ID', 'Performance'],
    title='Study Hours vs Final Exam Score'
)
st.plotly_chart(fig_scatter, use_container_width=True)

# -------------------------
# Radar Chart
# -------------------------
st.subheader("📡 Cluster Characteristics Radar Chart")

metrics = [
    'Study_Hours_per_Week',
    'Attendance_Percentage',
    'Assignments_Completed',
    'Mock_Test_Score',
    'Final_Exam_Score'
]

cluster_metrics_scaled = cluster_metrics.copy()
cluster_metrics_scaled[metrics] = (
    (cluster_metrics_scaled[metrics] - cluster_metrics_scaled[metrics].min()) /
    (cluster_metrics_scaled[metrics].max() - cluster_metrics_scaled[metrics].min()) * 100
)

fig_radar = go.Figure()
for _, row in cluster_metrics_scaled.iterrows():
    fig_radar.add_trace(go.Scatterpolar(
        r=row[metrics],
        theta=metrics,
        fill='toself',
        name=row['Cluster_Name']
    ))

fig_radar.update_layout(
    polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
    title="Cluster Comparison (Scaled)"
)
st.plotly_chart(fig_radar, use_container_width=True)

# -------------------------
# Cluster Percentage
# -------------------------
st.subheader("📈 Behavior Clusters")

cluster_counts = data['Cluster_Name'].value_counts().reset_index()
cluster_counts.columns = ['Cluster_Name', 'Students']
cluster_counts['Percentage'] = (
    cluster_counts['Students'] / cluster_counts['Students'].sum() * 100
).round(1)

for _, row in cluster_counts.iterrows():
    col1, col2 = st.columns([4, 1])
    col1.write(f"**{row['Cluster_Name']}**")
    col2.write(f"**{row['Percentage']}%**")
    st.markdown("---")

# -------------------------
# Cluster Insights
# -------------------------
st.subheader("🔍 Cluster Insights")

selected_cluster = st.selectbox(
    "Select Cluster",
    data['Cluster_Name'].unique()
)

cluster_row = cluster_metrics[
    cluster_metrics['Cluster_Name'] == selected_cluster
].iloc[0]

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Avg Study Hours", f"{cluster_row['Study_Hours_per_Week']:.2f}")
col2.metric("Avg Attendance %", f"{cluster_row['Attendance_Percentage']:.2f}")
col3.metric("Avg Assignments", f"{cluster_row['Assignments_Completed']:.2f}")
col4.metric("Avg Mock Score", f"{cluster_row['Mock_Test_Score']:.2f}")
col5.metric("Avg Final Score", f"{cluster_row['Final_Exam_Score']:.2f}")

# -------------------------
# Add New Student
# -------------------------
st.subheader("➕ Add New Student")

with st.form("add_student_form"):
    gender = st.selectbox("Gender", ["Female", "Male", "Others"])
    age = st.number_input("Age", 0, 100)

    study_hours = st.number_input("Study Hours per Week", 0, 100, 10)
    attendance = st.number_input("Attendance Percentage", 0, 100, 75)
    assignments = st.number_input("Assignments Completed", 0, 50, 10)

    previous_grade = st.number_input("Previous Grade", 0, 100, 10)
    internet_access = st.selectbox("Internet Access", ["Yes", "No"])

    mock_score = st.number_input("Mock Test Score", 0, 100, 60)
    final_score = st.number_input("Final Exam Score", 0, 100, 65)

    performance = st.selectbox("Performance", ["Excellent", "Poor", "Average"])

    submitted = st.form_submit_button("Add Student")

    if submitted:
        last_id = data['Student_ID'].iloc[-1]
        numeric_part = int(''.join(filter(str.isdigit, last_id)))
        new_id = f"STU{numeric_part + 1}"

        new_student = pd.DataFrame({
            'Student_ID': [new_id],
            'Gender': [gender],
            'Age': [age],
            'Study_Hours_per_Week': [study_hours],
            'Attendance_Percentage': [attendance],
            'Previous_Grade': [previous_grade],
            'Internet_Access': [internet_access],
            'Assignments_Completed': [assignments],
            'Mock_Test_Score': [mock_score],
            'Final_Exam_Score': [final_score],
            'Performance': [performance]
        })

        new_student_features = new_student[[
            'Study_Hours_per_Week',
            'Attendance_Percentage',
            'Assignments_Completed',
            'Mock_Test_Score',
            'Final_Exam_Score'
        ]]

        scaled_student = scaler.transform(new_student_features)
        cluster = kmeans.predict(scaled_student)[0]
        cluster_label = cluster_names[cluster]

        new_student['Cluster'] = cluster
        new_student['Cluster_Name'] = cluster_label

        st.session_state.data = pd.concat(
            [st.session_state.data, new_student],
            ignore_index=True
        )

        st.session_state.data.to_csv("Study_Track_AI_Project.csv", index=False)
        st.session_state.success_msg = "Student Added Successfully!"
        st.session_state.cluster_msg = cluster_label
        st.rerun()

# -------------------------
# Cluster Card Result
# -------------------------
if "success_msg" in st.session_state:
    st.success(st.session_state.success_msg)
    cluster_label = st.session_state.cluster_msg

    st.markdown(f"""
    <div style="
    background-color:#1f2937;
    padding:25px;
    border-radius:12px;
    box-shadow:0px 4px 12px rgba(0,0,0,0.3);
    color:white;
    text-align:center;
    margin-top:20px;
    ">
    <h2 style="color:#60a5fa;">🎯 Cluster Result</h2>
    <p style="font-size:22px;">
    <b>Category:</b> <span style="color:#34d399;">{cluster_label}</span>
    </p>
    <p style="font-size:16px;color:#d1d5db;">
    This student belongs to a study behavior group based on academic patterns.
    </p>
    </div>
    """, unsafe_allow_html=True)

    del st.session_state.success_msg
    del st.session_state.cluster_msg
