# utils/prompts.py
import streamlit as st

def get_initial_prompts(initial_prompt_a: str, initial_prompt_b: str):
    st.session_state.initial_prompt_a = initial_prompt_a
    st.session_state.initial_prompt_b = initial_prompt_b
