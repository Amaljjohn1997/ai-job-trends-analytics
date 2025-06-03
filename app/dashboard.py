# -*- coding: utf-8 -*-
"""
Created on Tue Jun  3 20:39:01 2025

@author: amalj
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter

# ── Load Data ──────────────────────────────
layoffs = pd.read_csv("data/layoffs.csv", parse_dates=["Date"])
jobs = pd.read_csv("data/job_postings.csv", parse_dates=["date"])

# ── Preprocessing ──────────────────────────
jobs["month"] = jobs["date"].dt.to_period("M").astype(str)
skills = jobs["skills"].dropna().str.split(",").explode().str.strip()
layoffs_by_industry = layoffs.groupby("Industry")["# Laid Off"].sum().sort_values(ascending=False)
job_posting_trend = jobs.groupby("month").size()
top_skills = pd.Series(Counter(skills)).sort_values(ascending=True).tail(10)

# ── Streamlit Config ───────────────────────
st.set_page_config(page_title="AI Job Trends", layout="wide")
st.markdown("<h1 style='text-align: center;'>📊 AI Job Trends Dashboard</h1>", unsafe_allow_html=True)

# ── Metrics Row ────────────────────────────
col1, col2, col3 = st.columns(3)
col1.metric("🔻 Total Layoffs", f"{layoffs['# Laid Off'].sum():,}")
col2.metric("📈 Total Postings", f"{len(jobs):,}")
col3.metric("💡 Top Skill", skills.mode()[0])

# ── Charts Row (2x2) ───────────────────────
col4, col5 = st.columns(2)

with col4:
    st.markdown("### 🔹 Layoffs by Industry")
    st.bar_chart(layoffs_by_industry)

with col5:
    st.markdown("### 🔹 Job Postings Over Time")
    st.line_chart(job_posting_trend)

col6, col7 = st.columns(2)

with col6:
    st.markdown("### 🔹 Top Skills in Demand")
    fig, ax = plt.subplots()
    top_skills.plot(kind='barh', ax=ax, color="lightgreen")
    ax.set_title("Top 10 Skills")
    st.pyplot(fig)

with col7:
    st.markdown("### 🔹 Filter by Location")
    location = st.selectbox("Choose Location", sorted(jobs["location"].unique()), key="loc")
    count = len(jobs[jobs["location"] == location])
    st.write(f"📍 Job Postings in {location}: **{count}**")
