import streamlit as st 
import pandas as pd
from preprocessing import preprocess_titanic_data

@st.cache_data
def load_data():
    data_raw = pd.read_csv('data/train.csv')
    data = preprocess_titanic_data(data_raw)
    return data