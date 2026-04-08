# 🎓 AI Student Study Tracking System

An AI-powered student study tracking web application built with **Streamlit** and **KMeans Clustering**. The system analyzes student academic behavior and provides personalized study recommendations based on their performance patterns.

---

## 🚀 Features

### 🔐 Authentication
- Role-based login system (Student / Admin)
- Secure password hashing with SHA-256
- Register using Student ID or Admin ID

### 🎓 Student Panel
- Personalized study recommendations based on cluster group
- Weekly study schedule and optimal study times
- Expected performance improvement chart
- Study session logging (date, subject, duration, distractions, quiz score)
- Study progress visualization over time
- AI Study Assistant chatbot for study-related queries

### ⚙️ Admin Panel
- System metrics — active students, study sessions, avg quiz score, dataset size
- CSV dataset upload and management
- KMeans model retraining (Quick Retrain + Full Retrain)
- Student behavior cluster visualization (Scatter Plot + Radar Chart)
- Dynamic cluster labeling based on Final Exam Score
- Add new students with automatic cluster assignment
- Analytics dashboard with EDA charts and correlation analysis

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Streamlit | Frontend & UI |
| Scikit-learn | KMeans Clustering, StandardScaler |
| Pandas & NumPy | Data Processing |
| Plotly | Interactive Charts |
| Hashlib (SHA-256) | Password Hashing |

---

## 📁 Project Structure

    project/
    ├── app.py
    ├── cluster_config.json
    ├── Study_Track_AI_Project.csv
    ├── student_logs.csv
    ├── users.json
    └── pages/
        ├── 0_Admin_Dashboard.py
        ├── 0_Study_Log_Sessions.py
        ├── 1_Student_Interface.py
        ├── 2_Admin_Panel.py
        └── 3_Analytics_Dashboard.py
## ⚙️ Installation

1. **Clone the repository**
```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
```

2. **Install dependencies**
```bash
pip install streamlit pandas numpy scikit-learn plotly
```

3. **Run the application**
```bash
streamlit run app.py
```

## 👤 How to Use

### Student
1. Register using your **Student ID** from the dataset
2. Login with your Student ID and password
3. View your personalized study recommendations
4. Log your daily study sessions
5. Track your progress over time using charts
6. Ask the AI Study Assistant for study tips

### Admin
1. Register using any **Admin ID**
2. Login with your Admin ID and password
3. View system metrics and student activity
4. Upload new datasets
5. Retrain the clustering model
6. Add new students and view their cluster assignment
7. Explore analytics and cluster insights

---

## 🤖 ML Model

- **Algorithm** — KMeans Clustering
- **Features used** — Study Hours per Week, Attendance Percentage, Assignments Completed, Mock Test Score, Final Exam Score
- **Cluster Labels** — Dynamically assigned based on average Final Exam Score ranking:
  - Needs Improvement → Low Engagement → Average Learner → Focused Studier → Consistent Performer → Good Performer → High Achiever → Top Performer → Outstanding Student → Elite Performer

---

## 📊 Dataset

The dataset (`Study_Track_AI_Project.csv`) contains the following columns:

| Column | Description |
|---|---|
| Student_ID | Unique student identifier |
| Gender | Student gender |
| Age | Student age |
| Study_Hours_per_Week | Weekly study hours |
| Attendance_Percentage | Class attendance % |
| Assignments_Completed | Number of assignments done |
| Previous_Grade | Previous academic grade |
| Internet_Access | Internet availability |
| Mock_Test_Score | Mock test score |
| Final_Exam_Score | Final exam score |
| Performance | Overall performance label |

