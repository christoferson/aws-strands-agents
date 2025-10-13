"""
=============================================================================
STRANDS AGENT DEMO - Custom Tools & Built-in Tools Integration
=============================================================================

This demo showcases how to create an AI agent using the Strands framework with:
- Built-in tools from the strands-tools package (calculator, current_time)
- A custom tool defined as a Python function (letter_counter)

The agent can handle multiple requests in a single conversation, automatically
selecting and using the appropriate tools to answer questions about:
- Current time
- Mathematical calculations
- Letter counting in words

This example demonstrates the flexibility of combining pre-built and custom
tools to create a versatile AI agent.
=============================================================================
"""

from strands import Agent, tool
from strands_tools import calculator, current_time

# Define a custom tool as a Python function using the @tool decorator
@tool
def letter_counter(word: str, letter: str) -> int:
    """
    Count occurrences of a specific letter in a word.

    Args:
        word (str): The input word to search in
        letter (str): The specific letter to count

    Returns:
        int: The number of occurrences of the letter in the word
    """
    if not isinstance(word, str) or not isinstance(letter, str):
        return 0

    if len(letter) != 1:
        raise ValueError("The 'letter' parameter must be a single character")

    return word.lower().count(letter.lower())

# Create an agent with tools from the strands-tools example tools package
# as well as our custom letter_counter tool (python_repl removed)
agent = Agent(tools=[calculator, current_time, letter_counter])

print(agent.model.config)

# Ask the agent a question that uses the available tools
message = """
I have 3 requests:

1. What is the time right now?
2. Calculate 3111696 / 74088
3. Tell me how many letter R's are in the word "strawberry" 🍓
"""
agent(message)