from strands import Agent, tool
from strands.models import BedrockModel
from strands_tools import calculator, current_time

# Define custom tools using the @tool decorator
@tool
def count_letter_in_word(word: str, letter: str) -> dict:
    """
    Count how many times a specific letter appears in a word (case-insensitive).

    Args:
        word: The word to search in
        letter: The letter to count

    Returns:
        A dictionary with the word, letter, and count
    """
    count = word.lower().count(letter.lower())
    return {
        "word": word,
        "letter": letter,
        "count": count
    }

@tool
def reverse_string(text: str) -> str:
    """
    Reverse a string.

    Args:
        text: The text to reverse

    Returns:
        The reversed text
    """
    return text[::-1]

# Initialize the Bedrock model
bedrock_model = BedrockModel(
    model_id="us.anthropic.claude-sonnet-4-20250514-v1:0",
    region_name="us-east-1",
    temperature=0.3,
)

# Create agent with built-in and custom tools
agent = Agent(
    model=bedrock_model,
    system_prompt="You are a helpful assistant.",
    tools=[calculator, current_time, count_letter_in_word, reverse_string]
)

message = """
Please answer the following questions:

1. What is the time right now?
2. Calculate 3111696 / 74088
3. Tell me how many letter R's are in the word "strawberry" 🍓
4. Reverse the word "strawberry"
5. Calculate integral of x**2 + 2*x

Format your output in JSON.
"""

# Have a conversation
response = agent(message)
print(response)


####

# Basic arithmetic evaluation
result = agent.tool.calculator(expression="2 * sin(pi/4) + log(e**2)")
print(result)
# Equation solving
result = agent.tool.calculator(expression="x**2 + 2*x + 1", mode="solve")
print(result)

# Calculate derivative
result = agent.tool.calculator(
    expression="sin(x)",
    mode="derive",
    wrt="x",
    order=2
)
print(result)

# Calculate integral
result = agent.tool.calculator(
    expression="x**2 + 2*x",
    mode="integrate",
    wrt="x"
)
print(result)