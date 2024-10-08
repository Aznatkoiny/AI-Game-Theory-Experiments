# utils/visualization.py

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def plot_payoff_over_rounds(df_results: pd.DataFrame):
    fig = px.line(
        df_results,
        x='Round',
        y=['Agent A Payoff', 'Agent B Payoff'],
        labels={'value': 'Payoff', 'Round': 'Round'},
        title="Prisoner's Dilemma Payoffs Over Rounds",
        hover_data={'Round': True, 'Agent A Payoff': ':.2f', 'Agent B Payoff': ':.2f'}
    )
    fig.update_layout(
        legend_title_text='Agents',
        hovermode='x unified'
    )
    return fig

def plot_cumulative_payoffs(df_results: pd.DataFrame):
    df_results['Cumulative A Payoff'] = df_results['Agent A Payoff'].cumsum()
    df_results['Cumulative B Payoff'] = df_results['Agent B Payoff'].cumsum()
    fig = px.line(
        df_results,
        x='Round',
        y=['Cumulative A Payoff', 'Cumulative B Payoff'],
        labels={'value': 'Cumulative Payoff', 'Round': 'Round'},
        title="Cumulative Payoffs Over Rounds",
        hover_data={'Round': True, 'Cumulative A Payoff': ':.2f', 'Cumulative B Payoff': ':.2f'}
    )
    fig.update_layout(
        legend_title_text='Agents',
        hovermode='x unified'
    )
    return fig

def plot_decision_patterns_heatmap(df_results: pd.DataFrame):
    try:
        df_results['Combined Decision'] = df_results['Agent A Decision'] + " vs " + df_results['Agent B Decision']
        decision_counts = df_results['Combined Decision'].value_counts().reset_index()
        decision_counts.columns = ['Decision Combination', 'Count']
        fig = px.bar(
            decision_counts,
            x='Decision Combination',
            y='Count',
            labels={'Count': 'Number of Occurrences', 'Decision Combination': 'Decision Combination'},
            title="Decision Patterns Heatmap",
            color='Count',
            color_continuous_scale='Viridis',
            hover_data={'Count': True}
        )
        fig.update_layout(
            xaxis={'categoryorder':'total descending'},
            hovermode='closest'
        )
        return fig
    except Exception as e:
        logger.error(f"Error creating heatmap: {e}")
        return None

def plot_decision_counts(df_results: pd.DataFrame):
    try:
        strategy_counts_a = df_results["Agent A Decision"].value_counts().reset_index()
        strategy_counts_a.columns = ['Decision', 'Count']
        strategy_counts_b = df_results["Agent B Decision"].value_counts().reset_index()
        strategy_counts_b.columns = ['Decision', 'Count']

        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=strategy_counts_a['Decision'],
            y=strategy_counts_a['Count'],
            name='Agent A',
            marker_color='indianred'
        ))
        fig.add_trace(go.Bar(
            x=strategy_counts_b['Decision'],
            y=strategy_counts_b['Count'],
            name='Agent B',
            marker_color='lightsalmon'
        ))
        fig.update_layout(
            barmode='group',
            title="Decision Counts for Agents",
            xaxis_title="Decision",
            yaxis_title="Count",
            legend_title="Agents",
            hovermode='x unified'
        )
        return fig
    except Exception as e:
        logger.error(f"Error creating decision counts chart: {e}")
        return None

def visualize_results(df_results: pd.DataFrame, payoff_placeholder, cumulative_placeholder, heatmap_placeholder, decision_counts_placeholder, summary_placeholder):
    """
    Visualize the results of the Prisoner's Dilemma game using Plotly.

    Parameters:
    - df_results (pd.DataFrame): DataFrame containing the game results.
    - payoff_placeholder: Streamlit placeholder for the payoff over rounds chart.
    - cumulative_placeholder: Streamlit placeholder for the cumulative payoffs chart.
    - heatmap_placeholder: Streamlit placeholder for the decision patterns heatmap.
    - decision_counts_placeholder: Streamlit placeholder for the decision counts chart.
    - summary_placeholder: Streamlit placeholder for the game summary.
    """
    # Validate DataFrame
    required_columns = ["Round", "Agent A Decision", "Agent B Decision", "Agent A Payoff", "Agent B Payoff"]
    if not all(column in df_results.columns for column in required_columns):
        st.error("DataFrame is missing required columns for visualization.")
        logger.error("DataFrame missing required columns.")
        return

    # Initialize or increment a counter for unique keys
    if 'chart_update_counter' not in st.session_state:
        st.session_state.chart_update_counter = 0
    st.session_state.chart_update_counter +=1
    current_count = st.session_state.chart_update_counter

    # Summary analysis
    total_a = df_results["Agent A Payoff"].sum()
    total_b = df_results["Agent B Payoff"].sum()
    cooperative_rounds_a = df_results[df_results["Agent A Decision"] == "Cooperate"].shape[0]
    cooperative_rounds_b = df_results[df_results["Agent B Decision"] == "Cooperate"].shape[0]

    with summary_placeholder:
        st.markdown("### **Game Summary**")
        st.write(f"**Total Payoff for Agent A:** {total_a}")
        st.write(f"**Total Payoff for Agent B:** {total_b}")
        st.write(f"**Agent A Cooperated:** {cooperative_rounds_a} times out of {df_results.shape[0]}")
        st.write(f"**Agent B Cooperated:** {cooperative_rounds_b} times out of {df_results.shape[0]}")

    # Payoff Over Rounds - Line Chart
    st.markdown("### **Prisoner's Dilemma Payoffs Over Rounds**")
    fig_payoff = plot_payoff_over_rounds(df_results)
    payoff_placeholder.plotly_chart(fig_payoff, use_container_width=True, key=f"payoff_over_rounds_{current_count}")

    # Cumulative Payoff Over Rounds - Line Chart
    st.markdown("### **Cumulative Payoffs Over Rounds**")
    fig_cumulative = plot_cumulative_payoffs(df_results)
    cumulative_placeholder.plotly_chart(fig_cumulative, use_container_width=True, key=f"cumulative_payoffs_{current_count}")

    # Decision Patterns Heatmap
    st.markdown("### **Decision Patterns Heatmap**")
    fig_heatmap = plot_decision_patterns_heatmap(df_results)
    if fig_heatmap:
        heatmap_placeholder.plotly_chart(fig_heatmap, use_container_width=True, key=f"decision_patterns_heatmap_{current_count}")

    # Decision Counts Bar Chart
    st.markdown("### **Decision Counts for Agents**")
    fig_decision_counts = plot_decision_counts(df_results)
    if fig_decision_counts:
        decision_counts_placeholder.plotly_chart(fig_decision_counts, use_container_width=True, key=f"decision_counts_{current_count}")
