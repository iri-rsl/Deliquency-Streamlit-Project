# comparisons, distributions, drilldowns
import streamlit as st
from utils.io import load_data
from utils.viz import show_deep_drives

def show():
    st.markdown("## Deep Drives")
    
    data = load_data()
    show_deep_drives(data)
    st.markdown("---")
    st.subheader("Summary of Detailed Regional Analyses")

    st.markdown("""
    In this section, we delved into **specific regions** to uncover more granular insights about delinquency trends.  
    By focusing on individual areas, we observed how **local factors** and **departmental differences** influence reported offences.  
    Key observations include:
    - **Urban vs Rural Dynamics**: Urban departments consistently reported higher offence rates, likely due to population density and reporting practices.  
    - **Departmental Variability**: Even within the same region, departments showed significant differences in offence types and rates, highlighting the importance of localized analysis.
    - **Crime Type Distributions**: Certain offence categories were more prevalent in specific regions, suggesting targeted prevention strategies may be effective.  
    These deep dives emphasize that delinquency is a complex, multifaceted issue that varies widely across different contexts.
    """)