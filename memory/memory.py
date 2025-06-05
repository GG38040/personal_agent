"""Memory module for managing conversation history."""

import json
import os
from typing import List, Dict, Optional

# Define constants
MEMORY_FILE = "memory/chat.json"
MAX_MEMORY = 10

# Ensure memory directory exists
os.makedirs(os.path.dirname(MEMORY_FILE), exist_ok=True)


def retrieve_context() -> str:
    """
    Retrieve conversation context from memory file.
    
    Returns:
        str: Formatted conversation history
    """
    if not os.path.exists(MEMORY_FILE):
        return ""

    try:
        with open(MEMORY_FILE, "r") as f:
            data = json.load(f)
            return "\n".join(
                f"{m['role']}: {m['content']}" for m in data
            )
    except json.JSONDecodeError:
        return ""


def update_memory(user: str, agent: str) -> None:
    """
    Update conversation memory with new interactions.
    
    Args:
        user: User's input message
        agent: Agent's response message
    """
    chat = []
    
    if os.path.exists(MEMORY_FILE):
        try:
            with open(MEMORY_FILE, "r") as f:
                chat = json.load(f)
        except json.JSONDecodeError:
            chat = []

    # Add new messages
    chat.extend([
        {"role": "user", "content": user},
        {"role": "assistant", "content": agent}
    ])

    # Keep only the most recent messages
    with open(MEMORY_FILE, "w") as f:
        json.dump(chat[-MAX_MEMORY:], f, indent=2)


def search_memory(query: str) -> List[Dict[str, str]]:
    """
    Search conversation history for specific content.
    
    Args:
        query: Search term to look for in messages
    
    Returns:
        List[Dict[str, str]]: Matching messages
    """
    try:
        with open(MEMORY_FILE, "r") as f:
            chat = json.load(f)
            return [
                m for m in chat
                if query.lower() in m['content'].lower()
            ]
    except (json.JSONDecodeError, FileNotFoundError):
        return []