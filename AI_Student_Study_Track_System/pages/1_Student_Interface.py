import streamlit as st
import pandas as pd
import json
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import plotly.express as px

st.title("🎓 Student Interface")
st.subheader("Personalized Study Recommendation")

@st.cache_data
def load_data():
    return pd.read_csv("Study_Track_AI_Project.csv")

data = load_data()

features = data[[
    'Study_Hours_per_Week',
    'Attendance_Percentage',
    'Assignments_Completed',
    'Mock_Test_Score',
    'Final_Exam_Score'
]]

with open("cluster_config.json") as f:
    config = json.load(f)

n_clusters = config["n_clusters"]

scaler = StandardScaler()
X_scaled = scaler.fit_transform(features)

kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
data["Cluster"] = kmeans.fit_predict(X_scaled)

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

# -------------------------
# Use logged-in student ID
# -------------------------
student_id = st.session_state.username
st.info(f"📋 Student ID: **{student_id}**")

student_data = data[data["Student_ID"] == student_id]

if len(student_data) == 0:
    st.error("Student ID not found in dataset.")
    st.stop()

student = student_data.iloc[0]
cluster_label = student["Cluster_Name"]

st.success(f"Cluster Group: {student['Cluster']} — {cluster_label}")

# -------------------------
# Recommendation function
# -------------------------
def get_recommendation(cluster_name):

    if cluster_name in ["Top Performer", "Outstanding Student", "Elite Performer"]:
        return {
            "times": ["6:00-8:00 AM", "3:00-5:00 PM", "8:00-9:30 PM"],
            "duration": 100,
            "break": 15,
            "effectiveness": 95,
            "tools": ["Pomodoro Timer", "Advanced Notes", "Mock Tests", "Research Papers"],
            "schedule": [3.5, 3, 3.5, 3, 3, 2, 2],
            "improvement": [88, 91, 94, 97],
            "reason": "You are already excelling. Focus on mastery and advanced challenges."
        }

    elif cluster_name in ["Good Performer", "Consistent Performer", "High Achiever"]:
        return {
            "times": ["8:00-10:00 AM", "2:00-3:30 PM", "7:00-8:30 PM"],
            "duration": 90,
            "break": 15,
            "effectiveness": 85,
            "tools": ["Pomodoro Timer", "Focus Music", "Site Blocker", "Digital Notes"],
            "schedule": [3, 2.5, 3, 2, 2.5, 1.5, 2],
            "improvement": [75, 80, 85, 90],
            "reason": "Students with similar study patterns improved scores using structured sessions."
        }

    elif cluster_name in ["Average Learner", "Focused Studier"]:
        return {
            "times": ["9:00-11:00 AM", "4:00-6:00 PM"],
            "duration": 75,
            "break": 10,
            "effectiveness": 80,
            "tools": ["Pomodoro Timer", "Flashcards", "Digital Notes"],
            "schedule": [2, 2, 2.5, 2, 2, 1.5, 1],
            "improvement": [70, 75, 80, 85],
            "reason": "Regular revision sessions improve retention and boost scores steadily."
        }

    elif cluster_name == "Low Engagement":
        return {
            "times": ["7:00-9:00 PM"],
            "duration": 60,
            "break": 10,
            "effectiveness": 70,
            "tools": ["Focus Music", "Mind Maps", "Digital Notes"],
            "schedule": [1.5, 1.5, 2, 1.5, 2, 1, 1],
            "improvement": [65, 70, 75, 80],
            "reason": "Short evening sessions help maintain focus and build consistency."
        }

    else:  # Needs Improvement
        return {
            "times": ["6:30-8:00 AM", "5:00-7:00 PM"],
            "duration": 60,
            "break": 10,
            "effectiveness": 65,
            "tools": ["Flashcards", "Mind Maps", "Focus Music", "Digital Notes"],
            "schedule": [1.5, 1.5, 2, 1.5, 1.5, 1, 1],
            "improvement": [55, 63, 70, 78],
            "reason": "Start with short focused sessions on basics to build a strong foundation."
        }

rec = get_recommendation(cluster_label)

# -------------------------
# Layout
# -------------------------
left, right = st.columns([2, 1])

# -------------------------
# LEFT SIDE
# -------------------------
with left:
    st.subheader("Personalized Study Recommendations")
    st.markdown("### Your Weekly Study Plan")

    st.markdown("#### Optimal Study Times")
    for t in rec["times"]:
        st.success(t)

    st.markdown("#### Study Duration")
    st.write(
        f"{rec['duration']} minute sessions with {rec['break']} minute breaks maximize your focus"
    )

    st.progress(rec["effectiveness"] / 100)
    st.write(f"Effectiveness: **{rec['effectiveness']}%**")

    st.markdown("#### Break Schedule")
    st.write(
        f"Take a {rec['break']} minute break every 25 minutes during study sessions"
    )

    st.markdown("#### Why this recommendation?")
    st.info(rec["reason"])

# -------------------------
# RIGHT SIDE
# -------------------------
with right:
    st.subheader("Recommended Study Tools")
    for tool in rec["tools"]:
        st.write(f"• {tool}")

    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    schedule_df = pd.DataFrame({
        "Day": days,
        "Hours": rec["schedule"]
    })

    fig1 = px.bar(
        schedule_df,
        x="Day",
        y="Hours",
        title="Weekly Study Schedule"
    )
    st.plotly_chart(fig1, use_container_width=True)

    # ← fix: fig2 now correctly inside 'with right' block
    improvement_df = pd.DataFrame({
        "Week": [1, 2, 3, 4],
        "Score": rec["improvement"]
    })

improvement_df = pd.DataFrame({
    "Week": [1, 2, 3, 4],
    "Score": rec["improvement"]
})

fig2 = px.line(
    improvement_df,
    x="Week",
    y="Score",
    markers=True,
    title="Expected Performance Improvement"
)

st.plotly_chart(fig2, use_container_width=True)

# -------------------------
# AI STUDY CHATBOT
# -------------------------
st.markdown("---")
st.header("AI Study Assistant 🤖")
st.write("Example questions: study plan, schedule, focus, concentrate, improve score, time management, motivation, lazy, remember, memory, exam preparation, stress, break, productive, night study, morning study, weak subject, revision, procrastination, health")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

def chatbot_response(question):
    q = question.lower()

    if "study plan" in q or "schedule" in q:
        return """Create a structured study plan:
- Divide subjects into small topics
- Study 60–90 minutes per session
- Take 10–15 minute breaks
- Review what you learned at the end of the day
- Practice mock tests weekly"""

    elif "focus" in q or "concentrate" in q:
        return """To improve focus while studying:
- Use the Pomodoro Technique (25 min study + 5 min break)
- Remove phone distractions
- Study in a quiet environment
- Set small goals for each session"""

    elif "improve score" in q or "improve marks" in q:
        return """Ways to improve your exam score:
- Revise concepts regularly
- Solve previous exam papers
- Practice mock tests
- Identify weak topics and focus on them
- Study consistently instead of last-minute preparation"""

    elif "time management" in q:
        return """Good time management tips:
- Create a daily study timetable
- Prioritize difficult subjects first
- Avoid multitasking
- Use timers to stay focused
- Track your study hours weekly"""

    elif "motivation" in q or "lazy" in q:
        return """To stay motivated:
- Set small achievable goals
- Reward yourself after completing tasks
- Track your progress
- Study with friends or group discussions
- Remember your long-term career goals"""

    elif "remember" in q or "memory" in q:
        return """Ways to improve memory:
- Use active recall
- Use flashcards
- Revise within 24 hours
- Teach concepts to someone else
- Use mind maps and diagrams"""

    elif "exam preparation" in q or "prepare for exam" in q:
        return """Exam preparation strategy:
1. Understand concepts clearly
2. Practice questions daily
3. Revise formulas and key points
4. Solve previous year question papers
5. Take mock tests under timed conditions"""

    elif "stress" in q or "anxiety" in q:
        return """To reduce exam stress:
- Take regular breaks
- Sleep 7–8 hours daily
- Exercise or walk daily
- Practice deep breathing
- Avoid studying continuously for long hours"""

    elif "break" in q:
        return """Breaks are important for productivity.
Recommended pattern:
- Study 25–50 minutes
- Take 5–10 minute break
- After 4 sessions take a longer break (20–30 min)"""

    elif "productive" in q:
        return """To be more productive:
- Study at the same time every day
- Remove distractions
- Track daily study progress
- Use active learning techniques"""

    elif "night study" in q:
        return """If you prefer night study:
- Study between 7 PM – 10 PM
- Avoid heavy meals before studying
- Keep lighting bright
- Sleep properly after studying"""

    elif "morning study" in q:
        return """Morning study benefits:
- Brain is fresh
- Better concentration
- Good for difficult subjects like math or programming
- Best time: 6 AM – 9 AM"""

    elif "weak subject" in q:
        return """To improve weak subjects:
- Start with basic concepts
- Practice problems daily
- Watch tutorials
- Ask doubts from teachers or friends"""

    elif "revision" in q:
        return """Effective revision method:
- Revise within 24 hours
- Revise again after 1 week
- Practice questions
- Use summary notes"""

    elif "procrastination" in q or "procrastinate" in q:
        return """To stop procrastination:
- Start with small tasks
- Use a 5-minute rule (just start studying)
- Remove distractions
- Create deadlines"""

    elif "health" in q or "sleep" in q:
        return """Healthy habits for students:
- Sleep 7–8 hours
- Drink enough water
- Eat healthy food
- Exercise daily
- Avoid late-night phone use"""

    else:
        return """I'm here to help you improve your study habits.
You can ask questions about:
- Study plans
- Time management
- Exam preparation
- Improving marks
- Focus and productivity
- Motivation
- Stress management"""

prompt = st.chat_input("Ask study related questions...")

if prompt:
    st.chat_message("user").write(prompt)
    response = chatbot_response(prompt)
    st.chat_message("assistant").write(response)
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.messages.append({"role": "assistant", "content": response})
