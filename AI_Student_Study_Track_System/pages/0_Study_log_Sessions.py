import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date

LOG_FILE = "student_logs.csv"

try:
    logs = pd.read_csv(LOG_FILE)
except:
    logs = pd.DataFrame(columns=[
        "Student_ID", "Date", "Study_Duration", "Subject", "Distractions", "Quiz_Score"
    ])

st.markdown("""
<div style="background:#8b6bdc;padding:20px;border-radius:10px;color:white;text-align:center;">
<h2>AI Student Study Tracking System</h2>
</div>
""", unsafe_allow_html=True)

st.subheader("📝 Study Log Sessions")

if not st.session_state.get("logged_in"):
    st.warning("Please log in to access this page.")
    st.stop()

student_id = st.session_state.username

st.markdown("### ➕ New Study Session")

with st.form("log_form"):
    col1, col2 = st.columns(2)

    with col1:
        log_date = st.date_input("Date", date.today())
        subject = st.selectbox("Subject", ["Math", "Science", "Programming", "English"])

    with col2:
        duration = st.number_input("Study Duration (minutes)", 0, 300, 60)
        distractions = st.selectbox("Distractions", ["None", "Phone", "Social Media", "Noise"])

    quiz_score = st.slider("Quiz Score (%)", 0, 100, 70)

    if st.form_submit_button("💾 Save Session"):
        new_log = pd.DataFrame({
            "Student_ID": [student_id],
            "Date": [log_date],
            "Study_Duration": [duration],
            "Subject": [subject],
            "Distractions": [distractions],
            "Quiz_Score": [quiz_score]
        })

        logs = pd.concat([logs, new_log], ignore_index=True)
        logs.to_csv(LOG_FILE, index=False)
        st.success("✅ Session saved successfully!")
        st.rerun()

st.markdown("### 📈 Your Study History")

student_logs = logs[logs["Student_ID"] == student_id]

if len(student_logs) > 0:
    student_logs = student_logs.copy()
    student_logs["Date"] = pd.to_datetime(student_logs["Date"])

    fig = px.line(
        student_logs.sort_values("Date"),
        x="Date",
        y=["Study_Duration", "Quiz_Score"],
        markers=True,
        title="Study Progress Over Time"
    )
    st.plotly_chart(fig, use_container_width=True)

    avg_score = student_logs["Quiz_Score"].mean()
    avg_duration = student_logs["Study_Duration"].mean()

    col1, col2, col3 = st.columns(3)
    col1.metric("📊 Avg Quiz Score", f"{avg_score:.1f}%")
    col2.metric("⏱️ Avg Study Time", f"{avg_duration:.0f} min")
    col3.metric("📅 Total Sessions", len(student_logs))

    if avg_score >= 85:
        st.info("🚀 **Advanced practice recommended**")
    elif avg_score >= 70:
        st.info("📚 **Revision + Practice needed**")
    else:
        st.warning("🔧 **Focus on basics first**")
else:
    st.info("📭 **No study sessions logged yet.** Start by adding your first session!")
