# utils/download.py

import pandas as pd
import streamlit as st

def download_results(df: pd.DataFrame):
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download Results as CSV",
        data=csv,
        file_name='prisoners_dilemma_results.csv',
        mime='text/csv',
    )
