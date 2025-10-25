# insights, implications, next steps
import streamlit as st
import streamlit as st

def show():
    st.title("Conclusions & Reflections")

    st.markdown("""
    ### 🧩 Key Takeaways
    - Reported delinquency in France has remained **relatively stable** over the past decade.  
    - **Regional contrasts** exist, with urban areas generally showing higher rates — 
      likely linked to population density and reporting frequency.  
    - The data highlights **patterns of reporting**, not necessarily patterns of crime.

    ### 🧠 Interpretation
    - High reported rates may reflect **greater reporting activity**, a greater police presence or a culture closer to trust in authorities, rather than higher actual delinquency.
    - **Underreporting** remains a significant issue, especially for sensitive crimes.
    - The dataset underrepresents the **true complexity** of delinquency. Indeed, there seems to be missing data for certain cases and types of offences.
                
    ### 🚀 Next Steps
    - Compare these results with **socioeconomic indicators** (unemployment, education, density) for real insights on delinquency drivers.
    - Integrate **victimization survey data** to capture unreported offences.  
    - Examine **seasonal or pandemic-related changes** in crime reports.
    - Explore **qualitative research** to understand underreporting and public perception.


    ---
    Thank you for exploring this dashboard!  
    Hopefully it provided a clearer, more balanced view of how reported delinquency evolves across France.
    """)
