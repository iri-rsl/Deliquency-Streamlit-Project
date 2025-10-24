# KPIs, high-level trends
import streamlit as st
import plotly.express as px
from utils.io import load_data
from utils.viz import show_kpis


def show():
    st.markdown("## Overview")
    # Load data
    data = load_data()
    st.markdown("### Summary of Key Performance Indicators (KPIs)")

    show_kpis(data)
    st.write("---")
    
    st.markdown("### How has reported delinquency evolved in France over time?")

    st.markdown("### How does population size relate to delinquency rate?")
    
    st.markdown("### Where are offences most concentrated geographically?")

    st.markdown("### What are the top types of reported offences?")

    
