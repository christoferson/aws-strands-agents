from strands import Agent, tool
from strands_tools import calculator, current_time
import requests

@tool
def search_wikipedia(query: str, sentences: int = 5) -> str:
    """
    Search Wikipedia and get a summary of the topic.

    Args:
        query (str): The search term or topic to look up on Wikipedia
        sentences (int): Number of sentences to return in the summary (default: 5)

    Returns:
        str: A summary of the Wikipedia article or search results
    """
    try:
        # Wikipedia API endpoint
        api_url = "https://en.wikipedia.org/api/rest_v1/page/summary/"

        # Add proper headers - Wikipedia requires a User-Agent
        headers = {
            'User-Agent': 'StrandsBot/1.0 (Educational Purpose; Python/requests)',
            'Accept': 'application/json'
        }

        # URL encode the query and make request
        encoded_query = requests.utils.quote(query)
        response = requests.get(f"{api_url}{encoded_query}", headers=headers, timeout=10)
        response.raise_for_status()

        data = response.json()

        # Check if page exists
        if data.get('type') == 'https://mediawiki.org/wiki/HyperSwitch/errors/not_found':
            return f"No Wikipedia article found for '{query}'. Try a different search term."

        # Extract relevant information
        title = data.get('title', 'Unknown')
        extract = data.get('extract', 'No summary available.')
        url = data.get('content_urls', {}).get('desktop', {}).get('page', '')

        # Limit extract to requested number of sentences
        sentences_list = extract.split('. ')
        if len(sentences_list) > sentences:
            extract = '. '.join(sentences_list[:sentences]) + '.'

        result = f"**{title}**\n\n{extract}\n\nRead more: {url}"

        return result

    except requests.exceptions.RequestException as e:
        return f"Error querying Wikipedia: {str(e)}"
    except Exception as e:
        return f"Error processing Wikipedia data: {str(e)}"

@tool
def get_wikipedia_content(title: str) -> str:
    """
    Get the full text content of a specific Wikipedia article.

    Args:
        title (str): The exact title of the Wikipedia article

    Returns:
        str: The full text content of the Wikipedia article
    """
    try:
        # Wikipedia API endpoint for full content
        api_url = "https://en.wikipedia.org/w/api.php"

        # Add proper headers - Wikipedia requires a User-Agent
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

        # Get the first (and should be only) page
        page = next(iter(pages.values()))

        if 'missing' in page:
            return f"No Wikipedia article found with title '{title}'."

        extract = page.get('extract', 'No content available.')
        page_title = page.get('title', title)

        # Limit content length
        max_length = 10000
        if len(extract) > max_length:
            extract = extract[:max_length] + "\n\n[Content truncated due to length...]"

        result = f"**{page_title}**\n\n{extract}"

        return result

    except requests.exceptions.RequestException as e:
        return f"Error fetching Wikipedia content: {str(e)}"
    except Exception as e:
        return f"Error processing Wikipedia content: {str(e)}"

# Create an agent with basic tools plus Wikipedia tools
agent = Agent(tools=[calculator, current_time, search_wikipedia, get_wikipedia_content])

print(agent.model.config)


# Example usage with Wikipedia
wiki_message = "Search Wikipedia for 'Artificial Intelligence' and give me a summary."
agent(wiki_message)

# wiki_message2 = "Get the full Wikipedia article about 'Machine Learning' and tell me about its history."
# agent(wiki_message2)