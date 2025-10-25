# load_data(), fetch_and_cache(), license text
import pandas as pd
import streamlit as st
import os
from utils.prep import clean_data

# -------------------------------------------------------------------
# CONFIGURATION
# -------------------------------------------------------------------

DATA_PATH = "data/delinquency.csv"   # adjust to your dataset name
DATA_URL = "https://www.data.gouv.fr/datasets/bases-statistiques-communale-departementale-et-regionale-de-la-delinquance-enregistree-par-la-police-et-la-gendarmerie-nationales/#/resources/93438d99-b493-499c-b39f-7de46fa58669"
LICENSE_TEXT = "DEP - Base statistique départementale de la délinquance enregistrée par la police et la gendarmerie nationales"
LICENSE_SOURCE = "Data.gouv.fr - Licence Ouverte / Open Licence v2.0"

# -------------------------------------------------------------------
# LOAD DATA FUNCTION
# -------------------------------------------------------------------
@st.cache_data(show_spinner=False)
def load_data() -> pd.DataFrame:
    """
    Load the raw delinquency dataset from local file.
    Cached to avoid reloading on every app refresh.
    """
    if os.path.exists(DATA_PATH):
        data = pd.read_csv(DATA_PATH, sep=";"
    )
        new_data = clean_data(data)
    else:
        st.error("❌ Dataset not found. Please place it in the /data folder.")
        return pd.DataFrame()
    return new_data

def load_raw_data() -> pd.DataFrame:
    """
    Load the raw delinquency dataset from local file without caching.
    Useful for debugging or when data changes frequently.
    """
    if os.path.exists(DATA_PATH):
        data = pd.read_csv(DATA_PATH, sep=";")
    else:
        st.error("❌ Dataset not found. Please place it in the /data folder.")
        return pd.DataFrame()
    
    return data


# -------------------------------------------------------------------
# License / metadata helper
# -------------------------------------------------------------------
def show_license():
    """
    Display dataset license or metadata in the sidebar or footer.
    """
    st.sidebar.markdown("---")
    st.sidebar.caption("LICENSE / DATA SOURCE")
    st.sidebar.caption(LICENSE_TEXT)
    st.sidebar.caption(LICENSE_SOURCE)
    st.sidebar.link_button("Go to data source", DATA_URL, type="secondary")