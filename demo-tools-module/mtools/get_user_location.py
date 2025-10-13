# get_user_location.py

from strands.tools import tool
from strands.types.tools import ToolResult, ToolUse
from typing import Any

@tool(
    description="Get the user's current location based on their IP or profile",
)
def get_user_location(tool: ToolUse, **kwargs: Any) -> ToolResult:
    tool_use_id = tool["toolUseId"]
    user_id = tool["input"].get("user_id", "default")

    # Simulate location lookup
    user_locations = {
        "default": "New York",
        "user123": "London",
        "user456": "Tokyo"
    }

    location = user_locations.get(user_id, "New York")

    return {
        "toolUseId": tool_use_id,
        "status": "success",
        "content": [{"text": f"User location: {location}"}]
    }