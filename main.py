# main.py

import streamlit as st
import pandas as pd
from utils.gpt4 import get_openai_client, get_gpt4_decision, get_randomized_initial_prompts
from utils.game_logic import run_prisoners_dilemma_round, randomize_payoff_matrix, reset_game
from utils.visualization import visualize_results
from utils.download import download_results
from config import DEFAULT_PAYOFF_MATRIX

def main():
    st.title("Prisoner's Dilemma with GPT-4")

    # Initialize session state
    if 'agent_a_history' not in st.session_state:
        st.session_state.agent_a_history = []
    if 'agent_b_history' not in st.session_state:
        st.session_state.agent_b_history = []
    if 'results' not in st.session_state:
        st.session_state.results = []
    if 'payoff_matrix' not in st.session_state:
        st.session_state.payoff_matrix = DEFAULT_PAYOFF_MATRIX.copy()
    if 'openai_client' not in st.session_state:
        st.session_state.openai_client = None
    if 'initial_prompt_a' not in st.session_state:
        st.session_state.initial_prompt_a = (
            "You are Agent A, an altruistic participant in the Prisoner's Dilemma game. "
            "Your primary goal is to promote mutual cooperation and trust. "
            "Based on the previous decisions of Agent B, decide whether to 'Cooperate' or 'Defect'. "
            "If Agent B has cooperated in the last round, consider reciprocating cooperation to build trust."
        )
    if 'initial_prompt_b' not in st.session_state:
        st.session_state.initial_prompt_b = (
            "You are Agent B, an opportunistic participant in the Prisoner's Dilemma game. "
            "Your primary goal is to maximize your own payoff, even if it means occasionally defecting. "
            "Based on the previous decisions of Agent A, decide whether to 'Cooperate' or 'Defect'. "
            "If Agent A has defected in the last round, consider retaliating to discourage further defections."
        )

    # Sidebar for user inputs
    st.sidebar.header("Configuration")

    # User input for API key
    api_key = st.sidebar.text_input("Enter your OpenAI API key:", type="password")

    if api_key:
        if st.session_state.openai_client is None:
            st.session_state.openai_client = get_openai_client(api_key)

    # Payoff Matrix Configuration
    st.sidebar.subheader("Payoff Matrix Options")
    payoff_option = st.sidebar.selectbox(
        "Select Payoff Matrix Configuration:",
        ["Default", "High Mutual Cooperation", "Punishing Defection", "Asymmetrical", "Custom"]
    )
    
    if payoff_option == "Default":
        st.session_state.payoff_matrix = DEFAULT_PAYOFF_MATRIX.copy()
        st.sidebar.success("Payoff matrix set to Default.")
    elif payoff_option == "High Mutual Cooperation":
        st.session_state.payoff_matrix = {
            ('Cooperate', 'Cooperate'): (5, 5),
            ('Cooperate', 'Defect'): (0, 6),
            ('Defect', 'Cooperate'): (6, 0),
            ('Defect', 'Defect'): (1, 1),
        }
        st.sidebar.success("Payoff matrix set to High Mutual Cooperation.")
    elif payoff_option == "Punishing Defection":
        st.session_state.payoff_matrix = {
            ('Cooperate', 'Cooperate'): (3, 3),
            ('Cooperate', 'Defect'): (0, 5),
            ('Defect', 'Cooperate'): (5, 0),
            ('Defect', 'Defect'): (-1, -1),
        }
        st.sidebar.success("Payoff matrix set to Punishing Defection.")
    elif payoff_option == "Asymmetrical":
        st.session_state.payoff_matrix = {
            ('Cooperate', 'Cooperate'): (4, 4),
            ('Cooperate', 'Defect'): (1, 5),
            ('Defect', 'Cooperate'): (5, 1),
            ('Defect', 'Defect'): (2, 2),
        }
        st.sidebar.success("Payoff matrix set to Asymmetrical.")
    elif payoff_option == "Custom":
        st.sidebar.subheader("Custom Payoff Matrix")
        coop_coop = st.sidebar.number_input("Payoff for (Cooperate, Cooperate):", min_value=0, value=3)
        coop_defect = st.sidebar.number_input("Payoff for (Cooperate, Defect):", min_value=0, value=0)
        defect_coop = st.sidebar.number_input("Payoff for (Defect, Cooperate):", min_value=0, value=5)
        defect_defect = st.sidebar.number_input("Payoff for (Defect, Defect):", min_value=0, value=1)
        st.session_state.payoff_matrix = {
            ('Cooperate', 'Cooperate'): (coop_coop, coop_coop),
            ('Cooperate', 'Defect'): (coop_defect, defect_coop),
            ('Defect', 'Cooperate'): (defect_coop, coop_defect),
            ('Defect', 'Defect'): (defect_defect, defect_defect),
        }
        st.sidebar.success("Payoff matrix set to Custom.")

    # Toggle for remembering previous rounds
    remember_history = st.sidebar.checkbox("Remember previous rounds", value=True)

    # Number of rounds to play
    num_rounds = st.sidebar.slider("Number of Rounds", min_value=1, max_value=100, value=10)

    # Initial Prompts Configuration
    st.sidebar.subheader("Initial Prompts")
    if st.sidebar.button("Randomize Initial Prompts"):
        if st.session_state.openai_client:
            initial_prompt_a, initial_prompt_b = get_randomized_initial_prompts(st.session_state.openai_client)
            st.session_state.initial_prompt_a = initial_prompt_a
            st.session_state.initial_prompt_b = initial_prompt_b
            st.sidebar.success("Initial prompts randomized.")
        else:
            st.sidebar.error("Please enter a valid OpenAI API key to randomize prompts.")
    else:
        initial_prompt_a = st.sidebar.text_area(
            "Initial prompt for Agent A:",
            value=st.session_state.get('initial_prompt_a'),
            height=100
        )
        initial_prompt_b = st.sidebar.text_area(
            "Initial prompt for Agent B:",
            value=st.session_state.get('initial_prompt_b'),
            height=100
        )
        st.session_state.initial_prompt_a = initial_prompt_a
        st.session_state.initial_prompt_b = initial_prompt_b

    # Buttons for running and resetting the game
    st.sidebar.subheader("Game Controls")
    run_game = st.sidebar.button("Run Game")
    reset = st.sidebar.button("Reset Game")

    if reset:
        reset_game()
        st.session_state.openai_client = None  # Reset the client

    if st.session_state.openai_client:
        if run_game:
            if st.session_state.results:
                st.warning("Game already run. Reset the game to start a new session.")
            else:
                with st.spinner("Running the game..."):
                    agent_a_history = st.session_state.agent_a_history
                    agent_b_history = st.session_state.agent_b_history
                    results = st.session_state.results

                    # Create separate placeholders for each chart
                    payoff_placeholder = st.empty()
                    cumulative_placeholder = st.empty()
                    heatmap_placeholder = st.empty()
                    decision_counts_placeholder = st.empty()
                    summary_placeholder = st.empty()
                    progress_bar = st.progress(0)

                    client = st.session_state.openai_client

                    for round_num in range(num_rounds):
                        decision_a, decision_b = run_prisoners_dilemma_round(
                            client,
                            agent_a_history,
                            agent_b_history,
                            remember_history,
                            st.session_state.initial_prompt_a,
                            st.session_state.initial_prompt_b
                        )

                        if decision_a is None or decision_b is None:
                            st.error("Error in getting decisions. Stopping the game.")
                            break

                        payoff_a, payoff_b = st.session_state.payoff_matrix.get(
                            (decision_a, decision_b),
                            (0, 0)  # Default payoffs if combination not found
                        )

                        agent_a_history.append(decision_a)
                        agent_b_history.append(decision_b)
                        results.append((round_num + 1, decision_a, decision_b, payoff_a, payoff_b))

                        # Update progress bar
                        progress_bar.progress((round_num + 1) / num_rounds)

                        # Real-time update
                        df_results = pd.DataFrame(results, columns=["Round", "Agent A Decision", "Agent B Decision", "Agent A Payoff", "Agent B Payoff"])
                        visualize_results(
                            df_results,
                            payoff_placeholder,
                            cumulative_placeholder,
                            heatmap_placeholder,
                            decision_counts_placeholder,
                            summary_placeholder
                        )

                    # Update session state
                    st.session_state.agent_a_history = agent_a_history
                    st.session_state.agent_b_history = agent_b_history
                    st.session_state.results = results

                # Final visualization
                df_results = pd.DataFrame(results, columns=["Round", "Agent A Decision", "Agent B Decision", "Agent A Payoff", "Agent B Payoff"])
                visualize_results(
                    df_results,
                    payoff_placeholder,
                    cumulative_placeholder,
                    heatmap_placeholder,
                    decision_counts_placeholder,
                    summary_placeholder
                )
                download_results(df_results)
        elif st.session_state.results:
            # Display results if already run
            df_results = pd.DataFrame(st.session_state.results, columns=["Round", "Agent A Decision", "Agent B Decision", "Agent A Payoff", "Agent B Payoff"])
            
            # Create separate placeholders for each chart
            payoff_placeholder = st.empty()
            cumulative_placeholder = st.empty()
            heatmap_placeholder = st.empty()
            decision_counts_placeholder = st.empty()
            summary_placeholder = st.empty()

            visualize_results(
                df_results,
                payoff_placeholder,
                cumulative_placeholder,
                heatmap_placeholder,
                decision_counts_placeholder,
                summary_placeholder
            )
            download_results(df_results)
    else:
        st.warning("Please enter your OpenAI API key to proceed.")

if __name__ == "__main__":
    main()
