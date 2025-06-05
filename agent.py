"""Agent module for handling OpenAI API interactions."""

import logging
from typing import Optional

import openai
from config import OPENAI_API_KEY

# Initialize the OpenAI client
client = openai.OpenAI(api_key=OPENAI_API_KEY)

# Configure logging
logging.basicConfig(
    filename='error.log',
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


def run_agent(user_input: str, memory_context: Optional[str] = None) -> str:
    """
    Process user input through the OpenAI API.
    
    Args:
        user_input: User's query or command
        memory_context: Previous conversation context
        
    Returns:
        str: Agent's response
    """
    try:
        system_prompt = open("prompts/system_prompt.txt").read()
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"{memory_context}\n{user_input}"}
        ]

        response = client.chat.completions.create(
            model="gpt-4",
            messages=messages
        )
        return response.choices[0].message.content

    except openai.APIError as e:
        logging.error("API Error: %s", str(e))
        return f"Error: {str(e)}"
    except Exception as e:
        logging.error("Unexpected Error: %s", str(e))
        return f"Error: {str(e)}"