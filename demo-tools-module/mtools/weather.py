from typing import Any
from strands.types.tools import ToolResult, ToolUse

TOOL_SPEC = {
    "name": "weather",
    "description": "Get weather information for a location",
    "inputSchema": {
        "json": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "City or location name"
                }
            },
            "required": ["location"]
        }
    }
}

# Function name must match tool name
def weather(tool: ToolUse, **kwargs: Any) -> ToolResult:
    tool_use_id = tool["toolUseId"]
    location = tool["input"]["location"]

    # Simulate weather lookup
    weather_data = {
        "New York": "Sunny, 72°F",
        "London": "Cloudy, 55°F",
        "Tokyo": "Rainy, 65°F",
        "Paris": "Partly cloudy, 68°F"
    }

    weather_info = weather_data.get(
        location, 
        f"Weather for {location}: Clear skies, 70°F"
    )

    return {
        "toolUseId": tool_use_id,
        "status": "success",
        "content": [{"text": weather_info}]
    }