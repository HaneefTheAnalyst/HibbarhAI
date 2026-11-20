import os
import requests

from dotenv import load_dotenv, find_dotenv
from langchain.tools import tool
from langchain.agents import create_agent
from langchain_groq import ChatGroq
from langchain_tavily import TavilySearch

# Load environment variables
load_dotenv(find_dotenv())


@tool
def get_weather_info(city: str) -> str:
    """Get current weather information for a city."""

    url = "https://api.apilayer.net/weatherstack/current"

    params = {
        "access_key": os.getenv("WEATHER_API_KEY"),
        "query": city
    }

    try:
        response = requests.get(
            url,
            params=params,
            timeout=15
        )
        response.raise_for_status()
        data = response.json()

        if "current" not in data:
            return f"Could not fetch weather for {city}."

        current = data["current"]
        location = data["location"]

        return (
            f"City: {location['name']}\n"
            f"Country: {location['country']}\n"
            f"Temperature: {current['temperature']}°C\n"
            f"Weather: {current['weather_descriptions'][0]}\n"
            f"Humidity: {current['humidity']}%"
        )

    except requests.RequestException as e:
        return f"Weather API error: {str(e)}"


# Initialize LLM
llm = ChatGroq(
    model=os.getenv("GROQ_MODEL"),
    temperature=0.3,
    max_retries=3
)

# Search tool
search_tool = TavilySearch(max_results=2)

# Create agent
agents = create_agent(
    model=llm,
    tools=[search_tool, get_weather_info],
    system_prompt="""
    You are an expert weather assistant.

    Your responsibilities:
    1. Find the capital of the requested country.
    2. Use the weather tool to retrieve its current weather.
    3. Present the information clearly.
    4. Never invent weather information.
    5. If a tool fails, explain that to the user.
    """
)


def ask_agent(question: str) -> str:

    result = agents.invoke({
        "messages": [
            {
                "role": "user",
                "content": question
            }
        ]
    })

    return result["messages"][-1].content

