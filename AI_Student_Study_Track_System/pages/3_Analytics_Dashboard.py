
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(layout="wide")

# -----------------------------
# Header Section
# -----------------------------
st.markdown("""
<div style='background-color:#3f51b5;padding:15px;border-radius:5px'>
<h2 style='color:white'>Analytics Dashboard </h2>
<p style='color:white'>
Module: Data Preprocessing & EDA • Explore patterns in study hours, test scores,
attendance and performance • Perform correlation analysis
</p>
</div>
""", unsafe_allow_html=True)

st.write("")

# -----------------------------
# Title + Buttons
# -----------------------------
col_title, col1, col2, col3 = st.columns([6,1,1,1])

with col_title:
    st.subheader("Student Behavior Analysis Dashboard")


# -----------------------------
# Load Dataset Automatically
# -----------------------------
df = pd.read_csv("Study_Track_AI_Project.csv")

# -----------------------------
# First Row
# -----------------------------
col1, col2 = st.columns(2)

# Study Hours vs Mock Test Score
with col1:

    fig1 = px.scatter(
        df,
        x="Study_Hours_per_Week",
        y="Mock_Test_Score",
        color="Performance",
        title="Study Time vs. Quiz Scores"
    )

    st.plotly_chart(fig1, use_container_width=True)

# Correlation Bubble Chart
with col2:

    numeric_df = df.select_dtypes(include=['int64','float64'])
    corr = numeric_df.corr()

    corr_df = corr.reset_index().melt(id_vars="index")
    corr_df.columns = ["Variable1","Variable2","Correlation"]

    fig2 = px.scatter(
        corr_df,
        x="Variable1",
        y="Variable2",
        size=abs(corr_df["Correlation"]),
        color="Correlation",
        size_max=40,
        title="Correlation Heatmap"
    )

    st.plotly_chart(fig2, use_container_width=True)

# -----------------------------
# Second Row
# -----------------------------
col3, col4 = st.columns(2)

# Attendance vs Performance
with col3:

    perf_att = df.groupby("Performance")["Attendance_Percentage"].mean().reset_index()

    fig3 = px.bar(
        perf_att,
        x="Performance",
        y="Attendance_Percentage",
        color="Performance",
        title="Attendance vs Performance"
    )

    st.plotly_chart(fig3, use_container_width=True)

# Performance Distribution
with col4:

    perf_counts = df["Performance"].value_counts()

    fig4 = go.Figure(data=[go.Pie(
        labels=perf_counts.index,
        values=perf_counts.values,
        hole=0.5
    )])

    fig4.update_layout(title="Performance Distribution")

    st.plotly_chart(fig4, use_container_width=True)
