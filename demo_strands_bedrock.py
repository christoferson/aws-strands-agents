from strands import Agent
from strands.models import BedrockModel

bedrock_model = BedrockModel(
    model_id="us.anthropic.claude-sonnet-4-20250514-v1:0",
    region_name="us-east-1",
    temperature=0.3,
)

agent = Agent(
    model=bedrock_model,
    system_prompt="You are a helpful assistant."
)

print(agent.model.config)

# Have a conversation
print(agent("My name is John"))
print(agent("What's my name?"))  # Should remember "John"