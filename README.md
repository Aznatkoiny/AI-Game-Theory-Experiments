# Prisoner's Dilemma LLM Performance Dashboard

## Overview

This project provides a Streamlit-based dashboard for researchers to test and analyze the performance of Large Language Models (LLMs) in Game Theory scenarios, specifically the Prisoner's Dilemma. The current version focuses on testing GPT-4's decision-making capabilities in this classic game theory problem.

## Project Goals

1. Provide a user-friendly interface for researchers to set up and run Prisoner's Dilemma experiments using LLMs.
2. Visualize and analyze the results of these experiments in real-time.
3. Allow for customization of game parameters and initial prompts to test various scenarios.
4. Facilitate the comparison of different LLM models or versions in game theory contexts.

## Features

- Interactive Streamlit dashboard for experiment setup and visualization
- Integration with OpenAI's GPT-4 API for decision-making
- Customizable payoff matrices for different Prisoner's Dilemma variants
- Real-time visualization of game results, including:
  - Payoff over rounds
  - Cumulative payoffs
  - Decision patterns heatmap
  - Decision counts for each agent
- Option to remember or forget previous rounds' history
- Downloadable results in CSV format
- Randomized initial prompts for diverse agent behaviors

## Prerequisites

- Python 3.7+
- OpenAI API key

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/your-username/prisoners-dilemma-llm-dashboard.git
   cd prisoners-dilemma-llm-dashboard
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Usage

1. Run the Streamlit app:
   ```
   streamlit run main.py
   ```

2. Open your web browser and navigate to the URL provided by Streamlit (usually `http://localhost:8501`).

3. Enter your OpenAI API key in the sidebar.

4. Configure the experiment parameters:
   - Select a payoff matrix from the dropdown or create a custom one:
     - Default: Classic Prisoner's Dilemma payoffs
     - High Mutual Cooperation: Encourages cooperation
     - Punishing Defection: Heavily penalizes mutual defection
     - Asymmetrical: Different payoffs for each agent
     - Custom: Define your own payoff values
   - Choose the number of rounds to play
   - Decide whether to remember previous rounds
   - Customize initial prompts for each agent or use randomized prompts

5. Click "Run Game" to start the experiment.

6. Analyze the results in real-time through the provided visualizations.

7. Download the results as a CSV file for further analysis.

## Project Structure

- `main.py`: The main Streamlit application file
- `utils/`:
  - `game_logic.py`: Contains the core game logic for the Prisoner's Dilemma
  - `gpt4.py`: Handles interactions with the GPT-4 API
  - `visualization.py`: Creates visualizations for the dashboard
  - `download.py`: Manages the download of results
- `config.py`: Contains default configurations and constants
- `requirements.txt`: Lists all Python dependencies

## Customization

Researchers can customize various aspects of the experiment:

- Payoff Matrix: Choose from preset matrices or create a custom one to test different game dynamics:
  1. Default: Classic Prisoner's Dilemma
     - (Cooperate, Cooperate): (3, 3)
     - (Cooperate, Defect): (0, 5)
     - (Defect, Cooperate): (5, 0)
     - (Defect, Defect): (1, 1)
  2. High Mutual Cooperation:
     - (Cooperate, Cooperate): (5, 5)
     - (Cooperate, Defect): (0, 6)
     - (Defect, Cooperate): (6, 0)
     - (Defect, Defect): (1, 1)
  3. Punishing Defection:
     - (Cooperate, Cooperate): (3, 3)
     - (Cooperate, Defect): (0, 5)
     - (Defect, Cooperate): (5, 0)
     - (Defect, Defect): (-1, -1)
  4. Asymmetrical:
     - (Cooperate, Cooperate): (4, 4)
     - (Cooperate, Defect): (1, 5)
     - (Defect, Cooperate): (5, 1)
     - (Defect, Defect): (2, 2)
  5. Custom: Define your own values for each outcome

- Initial Prompts: Modify the behavioral instructions given to each agent to explore different strategies.
- Number of Rounds: Adjust the game length to observe short-term or long-term behaviors.
- Memory: Toggle whether agents should consider the history of previous rounds in their decision-making.

## Future Enhancements

1. Integration with other LLM models for comparative analysis
2. Implementation of additional game theory scenarios (e.g., Ultimatum Game, Public Goods Game)
3. Advanced analytics and statistical tests for in-depth result analysis
4. Multi-agent scenarios with more than two players
5. Integration with external databases for long-term data storage and analysis

## Contributing

We welcome contributions to improve and expand this project. Please feel free to submit issues, feature requests, or pull requests.

## License

[MIT License](LICENSE)

## Acknowledgments

- OpenAI for providing the GPT-4 API
- Streamlit for the interactive dashboard framework
- The game theory community for ongoing research in this field

## Contact

For questions or feedback, please contact [Your Name] at [your.email@example.com].
