# context, objectives, and data caveats for the delinquency dashboard
import streamlit as st
from utils.io import show_license

def show ():
   st.title("Introduction: Beyond the Numbers")

   st.markdown("""
   ### 🧭 Context
   Delinquency is often a central topic in public debate in France, and statistics about it
   can easily influence perception — sometimes more than reality itself.
   This dashboard offers a simple, data-driven way to explore **how reported offences evolve**
   across regions and years, without jumping to conclusions.

   The goal is not to label regions as "dangerous" or "safe", but to **understand patterns**
   and **question what the data really tells us**.
   """)

   st.markdown("""
   ### 🎯 Objectives
   - Observe how delinquency indicators change over time.  
   - Compare regional differences across France.  
   - Encourage reflection on what reported data represents — and what it might hide.
   """)

   st.markdown("""
   ### ⚠️ Data Caveats & Limitations
   The dataset provides valuable insight into **reported offences**, but several caveats affect interpretation:

   1. **Reported offences only** — many incidents, especially minor or sensitive ones, go unreported.  
      This means the data reflects *institutional activity* more than actual delinquency levels.

   2. **Incomplete records** — some departments or years may contain missing or inconsistent data.

   3. **Population mismatch** — rates are computed with offence counts and population data from different years,  
      which may slightly distort values.

   4. **Possible duplicate reports** — without identifiers, the same incident may appear several times if multiple people report it.

   5. **Discrepancy between victim and infraction reports** —  
      official infraction data often differs from victimization reports.  
      For example, some women may declare domestic violence or assault but see their case dismissed for “lack of proof.”  
      These unrecognized or unpursued complaints **never appear in official infraction statistics**,  
      leading to a gap between **experienced** and **legally recorded** offences.

   In short, these figures should be read as **indicators of reported and recorded activity**,  
   not exact reflections of all experienced crime.
   """)

   st.markdown("### 🗂️ Dataset Information")

   st.info("""
   - We have a record of reported offences in France from 2016 to 2024
   - Data is broken down by department, offence type, and year
   - Data is also broken down by the different entities/actions involved: the victims, the act of infraction itself, the vehicles, and the perpetrators.

            For example, a single incident involving a stolen vehicle with an injured victim would generate multiple records: one for the victim, one for the vehicle, and one for the perpetrator.
   - Population data used to compute *taux pour mille* comes from INSEE census data of different years [2016-2021]
   """)

   st.markdown("""
   ---
   Use the **sidebar navigation** to explore:
   - National and regional trends  
   - Regional deep dives  
   - Data preparation and quality checks  
   - Final conclusions  
   """)
