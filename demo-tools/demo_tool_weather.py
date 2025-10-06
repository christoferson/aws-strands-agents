from strands import Agent, tool
from strands_tools import calculator, current_time
import requests

@tool
def get_weather(location: str) -> str:
    """
    Get current weather for any city worldwide.

    Args:
        location (str): City name (e.g., "London", "New York", "Tokyo")

    Returns:
        str: Current weather information including temperature, conditions, humidity, and wind
    """
    try:
        # Using wttr.in - completely free, no API key needed
        url = f"https://wttr.in/{location}?format=j1"
        headers = {'User-Agent': 'StrandsBot/1.0'}

        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        data = response.json()
        current = data['current_condition'][0]
        location_info = data['nearest_area'][0]

        city = location_info['areaName'][0]['value']
        country = location_info['country'][0]['value']
        temp_c = current['temp_C']
        temp_f = current['temp_F']
        desc = current['weatherDesc'][0]['value']
        humidity = current['humidity']
        wind_speed = current['windspeedKmph']
        feels_like_c = current['FeelsLikeC']
        feels_like_f = current['FeelsLikeF']

        result = f"**Weather in {city}, {country}:**\n\n"
        result += f"🌡️ Temperature: {temp_c}°C ({temp_f}°F)\n"
        result += f"🤔 Feels like: {feels_like_c}°C ({feels_like_f}°F)\n"
        result += f"☁️ Conditions: {desc}\n"
        result += f"💧 Humidity: {humidity}%\n"
        result += f"💨 Wind Speed: {wind_speed} km/h\n"

        return result

    except requests.exceptions.RequestException as e:
        return f"Error getting weather for '{location}'. Please check the city name and try again."
    except Exception as e:
        return f"Error processing weather data: {str(e)}"

# Create agent with all tools
agent = Agent(tools=[calculator, current_time, get_weather])

if __name__ == "__main__":
    print(agent.model.config)
    print("\n" + "="*80 + "\n")

    # Test 1: Time
    print("TEST 1: Current Time")
    print("-" * 80)
    agent("What time is it right now in Japan?")

    print("\n" + "="*80 + "\n")

    # Test 2: Calculator
    print("TEST 2: Calculator")
    print("-" * 80)
    agent("Calculate 1234 * 5678")

    print("\n" + "="*80 + "\n")

    # Test 3: Weather
    print("TEST 3: Weather")
    print("-" * 80)
    agent("What's the weather like in London?")

    print("\n" + "="*80 + "\n")

    # Test 4: Combined
    print("TEST 4: Combined Query")
    print("-" * 80)
    agent("What time is it, and what's the weather in Tokyo?")