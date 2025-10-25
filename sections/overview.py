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
    st.markdown("---")
    st.subheader("Summary of National & Regional Trends")

    st.markdown("""
    Overall, **reported delinquency in France shows moderate variation over the years**, 
    with some regions consistently above the national average and others remaining stable or improving.  
    Urban areas, as expected, tend to report higher rates — but this may reflect population density and reporting activity more than actual differences in behavior.

    Use the next section to **focus on specific regions** and explore their individual trends in detail.
    """)
    
