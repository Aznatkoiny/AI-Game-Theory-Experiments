# utils/game_logic.py

import random
import streamlit as st
from typing import List, Tuple
from utils.gpt4 import get_gpt4_decision

def run_prisoners_dilemma_round(
    client: "OpenAI",  # Import OpenAI from openai
    agent_a_history: List[str],
    agent_b_history: List[str],
    remember_history: bool,
    initial_prompt_a: str,
    initial_prompt_b: str
) -> Tuple[str, str]:
    if not agent_a_history or not remember_history:
        prompt_a = initial_prompt_a
        prompt_b = initial_prompt_b
    else:
        prompt_a = f"Given the previous decisions of Agent B: {agent_b_history}, what should Agent A choose (Cooperate or Defect)?"
        prompt_b = f"Given the previous decisions of Agent A: {agent_a_history}, what should Agent B choose (Cooperate or Defect)?"

    decision_a = get_gpt4_decision(client, prompt_a)
    decision_b = get_gpt4_decision(client, prompt_b)

    # Ensure decisions are valid
    decision_a = decision_a if decision_a in ["Cooperate", "Defect"] else "Cooperate"
    decision_b = decision_b if decision_b in ["Cooperate", "Defect"] else "Cooperate"

    return decision_a, decision_b

def randomize_payoff_matrix() -> dict:
    coop_coop = random.randint(1, 10)
    coop_defect = random.randint(0, 5)
    defect_coop = random.randint(5, 10)
    defect_defect = random.randint(0, 5)
    return {
        ('Cooperate', 'Cooperate'): (coop_coop, coop_coop),
        ('Cooperate', 'Defect'): (coop_defect, defect_coop),
        ('Defect', 'Cooperate'): (defect_coop, coop_defect),
        ('Defect', 'Defect'): (defect_defect, defect_defect),
    }

def reset_game():
    st.session_state.agent_a_history = []
    st.session_state.agent_b_history = []
    st.session_state.results = []
    st.session_state.payoff_matrix = {
        ('Cooperate', 'Cooperate'): (3, 3),
        ('Cooperate', 'Defect'): (0, 5),
        ('Defect', 'Cooperate'): (5, 0),
        ('Defect', 'Defect'): (1, 1),
    }
    st.success("Game has been reset.")
