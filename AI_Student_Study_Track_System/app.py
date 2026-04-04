import streamlit as st
import pandas as pd
import json
import hashlib

st.set_page_config(layout="wide")

# -------------------------
# FILES
# -------------------------
DATA_FILE = "Study_Track_AI_Project.csv"
USER_FILE = "users.json"

# -------------------------
# AUTH FUNCTIONS
# -------------------------
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def load_users():
    try:
        with open(USER_FILE) as f:
            return json.load(f)
    except:
        return {}

def save_users(users):
    with open(USER_FILE, "w") as f:
        json.dump(users, f)

# -------------------------
# SESSION INIT
# -------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = None
    st.session_state.role = None

# -------------------------
# LOAD DATA
# -------------------------
dataset = pd.read_csv(DATA_FILE)

try:
    with open("cluster_config.json") as f:
        config = json.load(f)
    cluster_labels = config["cluster_labels"]
except:
    cluster_labels = {}

# -------------------------
# LOGIN
# -------------------------
def login_page():
    st.title("🔐 Login")
    users = load_users()
    username = st.text_input("StudentID/AdminID")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username in users and users[username]["password"] == hash_password(password):
            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.role = users[username]["role"]
            st.success("Login Successful!")
            st.rerun()
        else:
            st.error("Invalid credentials")

# -------------------------
# REGISTER
# -------------------------
def register_page():
    st.title("📝 Register")
    new_id = st.text_input("Student ID / Admin ID")
    new_password = st.text_input("Create Password", type="password")
    role = st.selectbox("Role", ["student", "admin"])

    if st.button("Register"):
        users = load_users()
        if new_id in users:
            st.warning("User already exists!")
        elif new_id == "" or new_password == "":
            st.warning("Fields cannot be empty")
        else:
            if role == "student" and new_id not in dataset["Student_ID"].astype(str).values:
                st.error("Student ID not found in dataset!")
                return
            users[new_id] = {
                "password": hash_password(new_password),
                "role": role
            }
            save_users(users)
            st.success("Account created! Please login.")

# -------------------------
# BEFORE LOGIN
# -------------------------
if not st.session_state.logged_in:
    st.markdown("""
    <style>
        section[data-testid="stSidebar"] { display: none !important; }
    </style>
    """, unsafe_allow_html=True)

    menu = st.radio("Choose Option", ["Login", "Register"])
    if menu == "Login":
        login_page()
    else:
        register_page()

# -------------------------
# AFTER LOGIN
# -------------------------
else:
    role = st.session_state.role

    if role == "student":
        pages = [
            st.Page("pages/1_Student_Interface.py",   title="🎓 Student Dashboard"),
            st.Page("pages/0_Study_Log_Sessions.py",  title="📝 Study Log Sessions"),
        ]
    elif role == "admin":
        pages = [
            st.Page("pages/0_Admin_Dashboard.py",     title="⚙️ Admin Dashboard"),
            st.Page("pages/2_Admin_Panel.py",         title="🔧 Admin Panel"),
            st.Page("pages/3_Analytics_Dashboard.py", title="📊 Analytics Dashboard"),
        ]

    with st.sidebar:
        st.write(f"👤 **{st.session_state.username}**")
        st.write(f"📋 **Role:** {st.session_state.role.title()}")
        if st.button("🚪 Logout"):
            st.session_state.logged_in = False
            st.session_state.username = None
            st.session_state.role = None
            st.rerun()

    pg = st.navigation(pages, position="sidebar")
    pg.run()
