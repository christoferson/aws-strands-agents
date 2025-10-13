"""
=============================================================================
STRANDS AGENT DEMO - Tool Execution Strategies
=============================================================================

This demo showcases different tool execution strategies in the Strands framework:
- Concurrent execution (default): Tools run in parallel for better performance
- Sequential execution: Tools run one after another, useful when order matters

The demo includes:
- A mock weather tool that simulates API calls
- A mock time tool that gets current time
- A mock screenshot tool that simulates taking screenshots
- A mock email tool that simulates sending emails

This example demonstrates when to use concurrent vs sequential execution:
- Concurrent: Independent operations (weather + time lookup)
- Sequential: Dependent operations (screenshot → email the screenshot)

=============================================================================
"""

from strands import Agent, tool
from strands.tools.executors import SequentialToolExecutor
import time
from datetime import datetime

# Define mock tools for demonstration

@tool
def weather_tool(city: str) -> str:
    """
    Get the current weather for a specified city.

    Args:
        city (str): The name of the city to get weather for

    Returns:
        str: Weather information for the city
    """
    # Simulate API call delay
    time.sleep(0.5)

    # Mock weather data
    weather_data = {
        "New York": "Sunny, 72°F (22°C)",
        "London": "Cloudy, 59°F (15°C)",
        "Tokyo": "Rainy, 68°F (20°C)",
        "Paris": "Partly cloudy, 65°F (18°C)"
    }

    return weather_data.get(city, f"Weather data not available for {city}")


@tool
def time_tool(city: str) -> str:
    """
    Get the current time for a specified city.

    Args:
        city (str): The name of the city to get time for

    Returns:
        str: Current time in the city
    """
    # Simulate API call delay
    time.sleep(0.5)

    # Mock time data (in reality, you'd use timezone conversion)
    current_time = datetime.now().strftime("%I:%M %p")
    return f"Current time in {city}: {current_time}"


@tool
def screenshot_tool() -> str:
    """
    Take a screenshot of the current screen.

    Returns:
        str: Confirmation message with screenshot details
    """
    # Simulate screenshot capture delay
    time.sleep(1)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"screenshot_{timestamp}.png"

    return f"Screenshot captured successfully: {filename}"


@tool
def email_tool(recipient: str, subject: str, body: str, attachment: str = None) -> str:
    """
    Send an email with optional attachment.

    Args:
        recipient (str): Email address of the recipient
        subject (str): Email subject line
        body (str): Email body content
        attachment (str, optional): Path to file attachment

    Returns:
        str: Confirmation message
    """
    # Simulate email sending delay
    time.sleep(1)

    attachment_info = f" with attachment '{attachment}'" if attachment else ""
    return f"Email sent to {recipient}{attachment_info}. Subject: '{subject}'"


# =============================================================================
# DEMO 1: Concurrent Execution (Default)
# =============================================================================
print("\n" + "="*80)
print("DEMO 1: CONCURRENT EXECUTION (Default)")
print("="*80)
print("\nScenario: Getting weather and time for a city")
print("These operations are independent and can run in parallel.\n")

# Create agent with concurrent execution (default behavior)
concurrent_agent = Agent(tools=[weather_tool, time_tool])

start_time = time.time()
concurrent_agent("What is the weather and time in New York?")
concurrent_duration = time.time() - start_time

print(f"\n⏱️  Concurrent execution completed in: {concurrent_duration:.2f} seconds")
print("Note: Both tools ran in parallel, saving time!")


# =============================================================================
# DEMO 2: Sequential Execution
# =============================================================================
print("\n" + "="*80)
print("DEMO 2: SEQUENTIAL EXECUTION")
print("="*80)
print("\nScenario: Taking a screenshot and emailing it")
print("These operations are dependent - we need the screenshot before emailing.\n")

# Create agent with sequential execution
sequential_agent = Agent(
    tool_executor=SequentialToolExecutor(),
    tools=[screenshot_tool, email_tool]
)

start_time = time.time()
sequential_agent("Take a screenshot and email it to my friend at friend@example.com with subject 'Check this out'")
sequential_duration = time.time() - start_time

print(f"\n⏱️  Sequential execution completed in: {sequential_duration:.2f} seconds")
print("Note: Tools ran one after another, ensuring proper order!")


# =============================================================================
# DEMO 3: Comparison
# =============================================================================
print("\n" + "="*80)
print("EXECUTION STRATEGY COMPARISON")
print("="*80)
print(f"""
Concurrent Execution:
  ✓ Faster for independent operations
  ✓ Better resource utilization
  ✓ Default behavior
  ⏱️  Duration: {concurrent_duration:.2f}s

Sequential Execution:
  ✓ Ensures execution order
  ✓ Better for dependent operations
  ✓ Easier to debug
  ⏱️  Duration: {sequential_duration:.2f}s

Choose based on your use case:
- Use CONCURRENT when tools don't depend on each other
- Use SEQUENTIAL when one tool's output feeds into another
""")

print("="*80)
print("DEMO COMPLETE")
print("="*80)