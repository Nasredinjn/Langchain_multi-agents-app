from langchain.tools import tool
import requests
import trafilatura
from dotenv import load_dotenv
import os 
from tavily import TavilyClient
from rich import print
from typing import List
load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["TAVILY_API_KEY"] = os.getenv("TAVILY_API_KEY")

tavily_client = TavilyClient(api_key=os.environ["TAVILY_API_KEY"])


def web_search(query : str) -> str:
    """
    Perform a web search using the Tavily API.

    Args:
        query (str): The search query.

    Returns:
        list: The search results.
    """
    try:
        results : List[str] = []
        responses = tavily_client.search(query, max_results=5)
        for response in responses["results"]:
            results.append(f"""[bold green]Title:[/bold green] {response['title']}\n
                           [bold blue]URL:[/bold blue] {response['url']}\n
                           [bold yellow]Content:[/bold yellow] {response['content']}\n
                           """)
        return results
    except Exception as e:
        return f"An error occurred while performing the web search: {str(e)}"

def web_scrape(url: str) -> str:
    """Fetch a web page and return its readable text content.

    Args:
        url: The HTTP(S) URL to scrape.

    Returns:
        The page title followed by its extracted text, or an error message.
    """
    try:
        response = requests.get(
            url,
            headers={"User-Agent": "Mozilla/5.0 (compatible; WebScraper/1.0)"},
            timeout=15,
        )
        response.raise_for_status()

        content = trafilatura.extract(response.content, url=url)
        return content or "Could not extract readable content from this page."
    except requests.RequestException as error:
        return f"An error occurred while scraping {url}: {error}"
