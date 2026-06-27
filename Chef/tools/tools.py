import os

from dotenv import load_dotenv
from langchain_core.tools import tool
from tavily import TavilyClient


load_dotenv()

api_key = os.getenv("TAVILY_API_KEY")
if not api_key:
    raise RuntimeError(
        "TAVILY_API_KEY environment variable not set. Add it to a .env file or export it."
    )

tavily_client = TavilyClient(api_key=api_key)


@tool("recipe_search", description="find recipes based on available ingredients and dish type")
def recipe_search(ingredients: list[str], dish_type: str) -> str:
    """
    Args:
        ingredients: list of available ingredients
        dish_type: type of dish to cook
    """
    query = f"recipes for {', '.join(ingredients)} as {dish_type}"
    response = tavily_client.search(query)

    results = response.get("results", [])[:3]
    formatted = []

    for result in results:
        url = result.get("url", "")
        if "youtube.com" in url or "youtu.be" in url:
            continue

        formatted.append(
            f"Title: {result.get('title')}\n"
            f"URL: {result.get('url')}\n"
            f"Content: {result.get('content')}\n"
        )

    return "\n\n".join(formatted) if formatted else "No recipes found."
