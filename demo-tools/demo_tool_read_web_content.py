from strands import Agent, tool
from strands_tools import calculator, current_time
import requests
from bs4 import BeautifulSoup

@tool
def fetch_url_content(url: str) -> str:
    """
    Fetch and extract text content from a specified URL.

    Args:
        url (str): The URL to fetch content from

    Returns:
        str: The extracted text content from the webpage
    """
    try:
        # Set a user agent to avoid being blocked
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

        # Fetch the URL with a timeout
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        # Parse HTML content
        soup = BeautifulSoup(response.content, 'html.parser')

        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()

        # Get text content
        text = soup.get_text()

        # Clean up whitespace
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = '\n'.join(chunk for chunk in chunks if chunk)

        # Limit content length to avoid token limits
        max_length = 8000
        if len(text) > max_length:
            text = text[:max_length] + "\n\n[Content truncated due to length...]"

        return text

    except requests.exceptions.RequestException as e:
        return f"Error fetching URL: {str(e)}"
    except Exception as e:
        return f"Error processing content: {str(e)}"

# Create an agent with basic tools plus the URL fetcher
agent = Agent(tools=[calculator, current_time, fetch_url_content])

print(agent.model.config)

# Ask the agent a question that uses the available tools
message = """
Please fetch the content from https://en.wikipedia.org/wiki/Artificial_intelligence and give me a brief summary."
"""
agent(message)
