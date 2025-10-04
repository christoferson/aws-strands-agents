from strands import Agent
from strands.models import BedrockModel
from strands_tools import calculator, current_time, image_reader#, python_repl

bedrock_model = BedrockModel(
    model_id="us.anthropic.claude-sonnet-4-20250514-v1:0",
    region_name="us-east-1",
    temperature=0.3,
)

agent = Agent(
    model=bedrock_model,
    system_prompt="You are a helpful assistant.",
    tools=[calculator, current_time]
)

message = """
Please answer the following questions:

1. What is the time right now?
2. Calculate 3111696 / 74088
3. Tell me how many letter R's are in the word "strawberry" 🍓

Format your output in JSON.
"""

# Have a conversation
print(agent(message))