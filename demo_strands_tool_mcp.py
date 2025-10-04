from strands import Agent
from strands.models import BedrockModel
from strands_tools import calculator, current_time, image_reader#, python_repl
from strands.tools.mcp import MCPClient
from mcp.client.streamable_http import streamablehttp_client


mcp = MCPClient(
    lambda: streamablehttp_client("https://knowledge-mcp.global.api.aws")
)

bedrock_model = BedrockModel(
    model_id="us.anthropic.claude-sonnet-4-20250514-v1:0",
    region_name="us-east-1",
    temperature=0.3,
)

with mcp:
    agent = Agent(
        model=bedrock_model,
        system_prompt="You are a helpful assistant.",
        tools=[current_time, mcp.list_tools_sync()]
    )

    message = """
    Please answer the following questions:

    1. What is AgentCore runtime?
    2. How does AgentCore compare to Bedrock Agents?
    3. How does AgentCore compare to Strands Agents?

    Format your output in JSON.
    """

    # Have a conversation
    print(agent(message))