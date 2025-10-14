from strands import Agent
from mtools import get_user_location, weather, currency_converter


# Create agent with multiple tool modules
agent = Agent(
    tools=[get_user_location, weather, currency_converter],
    #model="claude-3-5-sonnet-20241022"
)

# Example 1: Using location and weather tools together
print("=== Example 1: Weather in my location ===")
response1 = agent("What is the weather like in my location?")
print(response1)

# Example 2: Weather in specific location
print("\n=== Example 2: Weather in London ===")
response2 = agent("What's the weather in London?")
print(response2)

# Example 3: Currency conversion
print("\n=== Example 3: Currency conversion ===")
response3 = agent("Convert 100 USD to EUR")
print(response3)

# Example 4: Complex multi-tool query
print("\n=== Example 4: Multi-tool query ===")
response4 = agent(
    "What's the weather in my location and how much is 50 USD in GBP?"
)
print(response4)