from strands import Agent, tool
from strands_tools import calculator, current_time
import requests

@tool
def search_wikipedia(query: str, limit: int = 5) -> str:
    """
    Search Wikipedia and return a list of related article titles.

    Args:
        query (str): The search term to look up on Wikipedia
        limit (int): Number of results to return (default: 5)

    Returns:
        str: A list of related Wikipedia article titles
    """
    try:
        api_url = "https://en.wikipedia.org/w/api.php"
        headers = {
            'User-Agent': 'StrandsBot/1.0 (Educational Purpose; Python/requests)',
            'Accept': 'application/json'
        }

        params = {
            'action': 'opensearch',
            'search': query,
            'limit': limit,
            'format': 'json'
        }

        response = requests.get(api_url, params=params, headers=headers, timeout=10)
        response.raise_for_status()

        data = response.json()
        titles = data[1]
        descriptions = data[2]
        urls = data[3]

        if not titles:
            return f"No Wikipedia articles found for '{query}'."

        result = f"**Wikipedia Search Results for '{query}':**\n\n"
        for i, (title, desc, url) in enumerate(zip(titles, descriptions, urls), 1):
            result += f"{i}. **{title}**\n"
            if desc:
                result += f"   {desc}\n"
            result += f"   {url}\n\n"

        return result

    except Exception as e:
        return f"Error searching Wikipedia: {str(e)}"

@tool
def get_wikipedia_summary(title: str) -> str:
    """
    Get a summary of a Wikipedia article.

    Args:
        title (str): The title of the Wikipedia article

    Returns:
        str: A summary of the Wikipedia article with URL
    """
    try:
        api_url = "https://en.wikipedia.org/api/rest_v1/page/summary/"
        headers = {
            'User-Agent': 'StrandsBot/1.0 (Educational Purpose; Python/requests)',
            'Accept': 'application/json'
        }

        encoded_title = requests.utils.quote(title)
        response = requests.get(f"{api_url}{encoded_title}", headers=headers, timeout=10)
        response.raise_for_status()

        data = response.json()

        if data.get('type') == 'https://mediawiki.org/wiki/HyperSwitch/errors/not_found':
            return f"No Wikipedia article found for '{title}'."

        page_title = data.get('title', 'Unknown')
        extract = data.get('extract', 'No summary available.')
        url = data.get('content_urls', {}).get('desktop', {}).get('page', '')

        result = f"**{page_title}**\n\n{extract}\n\nRead more: {url}"

        return result

    except Exception as e:
        return f"Error getting Wikipedia summary: {str(e)}"

@tool
def get_wikipedia_content(title: str) -> str:
    """
    Get the full text content of a Wikipedia article.

    Args:
        title (str): The title of the Wikipedia article

    Returns:
        str: The full text content of the Wikipedia article
    """
    try:
        api_url = "https://en.wikipedia.org/w/api.php"
        headers = {
            'User-Agent': 'StrandsBot/1.0 (Educational Purpose; Python/requests)',
            'Accept': 'application/json'
        }

        params = {
            'action': 'query',
            'format': 'json',
            'titles': title,
            'prop': 'extracts',
            'explaintext': True,
            'exsectionformat': 'plain'
        }

        response = requests.get(api_url, params=params, headers=headers, timeout=10)
        response.raise_for_status()

        data = response.json()
        pages = data.get('query', {}).get('pages', {})
        page = next(iter(pages.values()))

        if 'missing' in page:
            return f"No Wikipedia article found for '{title}'."

        extract = page.get('extract', 'No content available.')
        page_title = page.get('title', title)

        # Limit content length
        max_length = 10000
        if len(extract) > max_length:
            extract = extract[:max_length] + "\n\n[Content truncated due to length...]"

        # Get URL
        page_url = f"https://en.wikipedia.org/wiki/{requests.utils.quote(page_title.replace(' ', '_'))}"

        result = f"**{page_title}**\n\nURL: {page_url}\n\n{extract}"

        return result

    except Exception as e:
        return f"Error getting Wikipedia content: {str(e)}"

# Create agent with all tools
agent = Agent(tools=[
    calculator, 
    current_time, 
    search_wikipedia,
    get_wikipedia_summary,
    get_wikipedia_content
])

# Example usage
if __name__ == "__main__":
    print(agent.model.config)
    print("\n" + "="*80 + "\n")

    # Test 1: Search
    print("TEST 1: Search Wikipedia")
    print("-" * 80)
    agent("Search Wikipedia for 'Artificial Intelligence'.")

    print("\n" + "="*80 + "\n")

    # Test 2: Get summary
    print("TEST 2: Get Summary")
    print("-" * 80)
    agent("Get a summary of 'Machine Learning' from Wikipedia.")

    print("\n" + "="*80 + "\n")

    # Test 3: Full content
    print("TEST 3: Full Content")
    print("-" * 80)
    agent("Get the Wikipedia article about 'Python (programming language)' and tell me who created it.")

    print("\n" + "="*80 + "\n")

    # Test 4: Combined query
    print("TEST 4: Combined Query")
    print("-" * 80)
    agent("Search for 'Deep Learning', then get a summary of the first result.")