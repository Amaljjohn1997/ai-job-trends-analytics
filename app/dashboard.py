import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Job Market Trends Dashboard")

jobs = pd.read_csv("data/job_postings.csv", parse_dates=["date"])

selected_industry = st.selectbox("Choose Industry", jobs["industry"].unique())

filtered = jobs[jobs["industry"] == selected_industry]

st.write(f"Showing job postings for: {selected_industry}")
st.line_chart(filtered.groupby("date").size())
