# Data preparation visualization functions
import streamlit as st
from utils.io import load_data, load_raw_data
from utils.viz import show_missing_data, show_duplicates

def show():
    st.markdown("## Technical Section")
    st.write("This section focuses on data preparation and cleaning steps.")

    raw_data = load_raw_data()
    st.markdown("### Raw Data Overview")
    st.dataframe(raw_data.head())   
    show_missing_data(raw_data)
    show_duplicates(raw_data)

    st.markdown("### Data Cleaning Steps")
    st.write("Converted 'taux_pour_mille' to numeric, added department and region names for better context.")
    st.write("Nothing else changed as there were no duplicates to remove nor missing values.")

    st.write("---")
    st.write("## After the necessary conversion and additions:")
    cleaned_data = load_data()
    st.success(f"✅ Data loaded successfully! {cleaned_data.shape[0]} rows × {cleaned_data.shape[1]} columns.")
    st.info(f"Data columns: {', '.join(cleaned_data.columns)}")
    st.write("### Cleaned Data Overview")
    st.dataframe(cleaned_data.head())
