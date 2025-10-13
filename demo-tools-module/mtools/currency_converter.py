# currency_converter.py

from typing import Any
from strands.types.tools import ToolResult, ToolUse

TOOL_SPEC = {
    "name": "currency_converter",
    "description": "Convert amount from one currency to another",
    "inputSchema": {
        "json": {
            "type": "object",
            "properties": {
                "amount": {
                    "type": "number",
                    "description": "Amount to convert"
                },
                "from_currency": {
                    "type": "string",
                    "description": "Source currency code (e.g., USD)"
                },
                "to_currency": {
                    "type": "string",
                    "description": "Target currency code (e.g., EUR)"
                }
            },
            "required": ["amount", "from_currency", "to_currency"]
        }
    }
}

def currency_converter(tool: ToolUse, **kwargs: Any) -> ToolResult:
    tool_use_id = tool["toolUseId"]
    amount = tool["input"]["amount"]
    from_curr = tool["input"]["from_currency"]
    to_curr = tool["input"]["to_currency"]

    # Simplified conversion rates
    rates = {
        ("USD", "EUR"): 0.85,
        ("USD", "GBP"): 0.73,
        ("EUR", "USD"): 1.18,
        ("GBP", "USD"): 1.37
    }

    rate = rates.get((from_curr, to_curr), 1.0)
    converted = amount * rate

    result_text = f"{amount} {from_curr} = {converted:.2f} {to_curr}"

    return {
        "toolUseId": tool_use_id,
        "status": "success",
        "content": [{"text": result_text}]
    }