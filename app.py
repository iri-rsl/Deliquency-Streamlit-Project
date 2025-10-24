## Project of data analysis and visualization
# Author: Iriantsoa RASOLOARIVALONA
# Date: 18-10-2025
# Email: iriantsoa.rasoloarivalona@efrei.net
# Student ID: 20220747

from sections import intro, technical,  overview, deep_drives, conclusion
from utils.io import show_license
import streamlit as st

# Setting page configuration
st.set_page_config(page_title="Data Storytelling Dashboard", layout="wide")
st.title("Has France become safer in the past decade?")
st.write("An analysis of delinquency trends across French departments with data taken between 2016 and 2024.")

# Sidebar navigation
st.sidebar.header("Navigation")
st.sidebar.title("🚔 Delinquency Analysis")
page = st.sidebar.selectbox(
    "Choose a section to explore:", ["Introduction", "Technical Notes and Preparation", "National and regional trends", "Detailed regional analyses", "Final insights and conclusions"]
)
show_license()




# Load the selected page
if page == "Introduction":
    intro.show()
elif page == "Technical Notes and Preparation":
    technical.show()
elif page == "National and regional trends":
    overview.show()
elif page == "Detailed regional analyses":
    deep_drives.show()
elif page == "Final insights and conclusions":
    conclusion.show()



