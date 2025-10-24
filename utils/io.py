# load_data(), fetch_and_cache(), license text
import pandas as pd
import streamlit as st
import os

# -------------------------------------------------------------------
# Configuration
# -------------------------------------------------------------------

DATA_PATH = "data/delinquency.csv"   # adjust to your dataset name                  # if using an online dataset
LICENSE_TEXT = "Source: data.gouv.fr — Open Licence v2.0"  # adjust as needed


# -------------------------------------------------------------------
# Load raw data
# -------------------------------------------------------------------
@st.cache_data(show_spinner=True)
def load_data() -> pd.DataFrame:
    """
    Load the raw delinquency dataset from local file.
    Cached to avoid reloading on every app refresh.
    Returns:
        df (pd.DataFrame): Raw dataframe
    """
    if os.path.exists(DATA_PATH):
        data = pd.read_csv(DATA_PATH)
    else:
        st.error("❌ Dataset not found. Please place it in the /data folder.")
        return pd.DataFrame()

    st.success(f"✅ Data loaded successfully! {data.shape[0]} rows × {data.shape[1]} columns.")
    st.info(f"Data columns: {', '.join(data.columns)}")
    return data


# -------------------------------------------------------------------
# License / metadata helper
# -------------------------------------------------------------------
def show_license():
    """
    Display dataset license or metadata in the sidebar or footer.
    """
    st.markdown(f"**License:** {LICENSE_TEXT}")
