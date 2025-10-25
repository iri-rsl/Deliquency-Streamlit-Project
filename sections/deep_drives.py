# comparisons, distributions, drilldowns
import streamlit as st
from utils.io import load_data
from utils.viz import show_deep_drives

def show():
    st.markdown("## Deep Drives")
    
    data = load_data()
    show_deep_drives(data)
    