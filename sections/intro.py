# context, objectives, and data caveats for the delinquency dashboard
import streamlit as st
from utils.io import show_license

def show():
    # -------------------------------
    # Title
    # -------------------------------
    st.title("Delinquency in France: Beyond the Numbers")

    # -------------------------------
    # Context
    # -------------------------------
    st.markdown("""
    ### 🧭 Context

    Discussions about *delinquency* in France are never purely statistical.  
    Crime figures regularly fuel political debates, public fears, and sometimes, **stigmatization** of certain territories or populations.

    Yet, behind these numbers lies a more complex reality:  
    - Delinquency data depends on what is **reported**, **recorded**, and **classified**.  
    - A region with more active police reporting can appear *more delinquent* than another where crimes are underreported.  
    - Media narratives often amplify these differences, turning data into tools of perception rather than objective measurement.

    This dashboard does **not** aim to label regions as “safe” or “dangerous”.  
    Instead, it invites users to **observe trends critically**, understand the **limits of quantitative data**, and question how such numbers are produced and interpreted.
    """)

    # -------------------------------
    # Objectives
    # -------------------------------
    st.markdown("""
    ### 🎯 Objectives

    Using open data from [data.gouv.fr](https://www.data.gouv.fr/), this dashboard aims to:
    - Explore how **reported delinquency** has evolved across years and regions in France.  
    - Identify **regional differences** in offence rates, while keeping methodological limits in mind.  
    - Encourage **critical reflection** on what these numbers represent — and what they might conceal.  
    """)

    # -------------------------------
    # Data caveats
    # -------------------------------
    st.markdown("""
    ### ⚠️ Data Caveats & Limitations

    While the dataset offers valuable insight into reported offences, it must be interpreted with caution:

    1. **Reported offences only** — data covers only crimes officially reported to authorities;  
       unreported or unrecorded incidents are absent.

    2. **Incomplete records** — some years or departments may contain missing or inconsistent entries.

    3. **Population mismatch** — *taux pour mille* (rate per 1,000 inhabitants) is calculated from 
       offence counts and population data from **different years**, introducing approximation errors.

    4. **Possible duplicate reports** — since there are no identifiers, the same event could have been 
       reported several times or by multiple individuals.

    These limits mean that the figures shown here are **indicators of reported activity**,  
    not an exact measure of real or perceived delinquency.
    """)

    # -------------------------------
    # Dataset information
    # -------------------------------
    st.markdown("### 🗂️ Dataset Information")

    st.info("""
    - We have a record of reported offences in France from 2016 to 2024
    - Data is broken down by department, offence type, and year
    - Data is also broken down by the different entities/actions involved: the victims, the act of infraction itself, the vehicles, and the perpetrators.

            For example, a single incident involving a stolen vehicle with an injured victim would generate multiple records: one for the victim, one for the vehicle, and one for the perpetrator.
    - Population data used to compute *taux pour mille* comes from INSEE census data of different years [2016-2021]
    """)

    # -------------------------------
    # Navigation hint
    # -------------------------------
    st.markdown("""
    ---
    Use the **sidebar navigation** on the left 👈 to explore:
    - National and regional trends      
    - Regional deep dives  
    - Data preparation & quality checks  
    - Final insights and reflections  
    """)
