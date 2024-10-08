# utils/gpt4.py

import openai
import streamlit as st
import time
import logging
from typing import Tuple, Optional
from openai import OpenAI, AuthenticationError, RateLimitError, OpenAIError

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_openai_client(api_key: str) -> OpenAI:
    """
    Instantiate and return an OpenAI client with the provided API key.
    """
    return OpenAI(api_key=api_key)

def get_gpt4_decision(client: OpenAI, prompt: str, retries: int = 3, delay: int = 2) -> Optional[str]:
    """
    Send a prompt to GPT-4 and retrieve the decision ('Cooperate' or 'Defect').
    Implements retry logic for handling rate limits and other transient errors.
    """
    for attempt in range(retries):
        try:
            logger.info(f"Attempt {attempt + 1}: Sending prompt to GPT-4.")
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": prompt}
                ],
                max_tokens=10,
                temperature=0.8  # Increased for variability
            )
            # Extract the content from the response
            decision = response.choices[0].message.content.strip().lower()
            logger.info(f"Received decision: {decision}")
            if "cooperate" in decision:
                return "Cooperate"
            elif "defect" in decision:
                return "Defect"
            else:
                logger.warning(f"Unclear decision '{decision}'. Defaulting to Cooperate.")
                return "Cooperate"  # Default choice if response is unclear
        except AuthenticationError:
            logger.error("AuthenticationError: Invalid OpenAI API key.")
            st.error("Invalid OpenAI API key. Please enter a valid key.")
            return None
        except RateLimitError:
            logger.warning("RateLimitError: Rate limit exceeded. Retrying...")
            st.warning("Rate limit exceeded. Retrying...")
            time.sleep(delay)
        except OpenAIError as e:
            logger.error(f"OpenAIError: {e}")
            st.error(f"OpenAI API error: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            st.error(f"Unexpected error: {e}")
            return None
    logger.error("Failed to get a decision from GPT-4 after multiple attempts.")
    st.error("Failed to get a decision from GPT-4 after multiple attempts.")
    return "Cooperate"  # Default choice in case of repeated failures

def get_randomized_initial_prompts(client: OpenAI) -> Tuple[str, str]:
    """
    Generate two randomized initial prompts for Agent A and Agent B using GPT-4.
    """
    try:
        logger.info("Generating randomized initial prompts using GPT-4.")
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Generate two random unique scenarios for the Prisoner's Dilemma game, one for each agent. Each scenario should provide a unique role for the agent and end with the question 'Should you Cooperate or Defect?'."}
            ],
            max_tokens=150,
            temperature=0.8
        )
        # Extract content from the response
        content = response.choices[0].message.content.strip()
        prompts = [line.strip() for line in content.split('\n') if line.strip()]
        if len(prompts) >= 2:
            prompt_a = prompts[0]
            prompt_b = prompts[1]
            logger.info("Successfully generated two prompts.")
        else:
            prompt_a = prompt_b = "This is the first round of the Prisoner's Dilemma. Should you 'Cooperate' or 'Defect'?"
            logger.warning("Insufficient prompts generated. Using default prompts.")
        return prompt_a, prompt_b
    except OpenAIError as e:
        logger.error(f"OpenAIError: {e}")
        st.error(f"Error in getting randomized initial prompts from GPT-4: {e}")
        return (
            "This is the first round of the Prisoner's Dilemma. Should Agent A 'Cooperate' or 'Defect'?",
            "This is the first round of the Prisoner's Dilemma. Should Agent B 'Cooperate' or 'Defect'?"
        )
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        st.error(f"Unexpected error while generating prompts: {e}")
        return (
            "This is the first round of the Prisoner's Dilemma. Should Agent A 'Cooperate' or 'Defect'?",
            "This is the first round of the Prisoner's Dilemma. Should Agent B 'Cooperate' or 'Defect'?"
        )
