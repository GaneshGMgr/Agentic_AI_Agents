import requests
from langchain.tools import tool
from ddgs import DDGS
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv
from langchain_tavily import TavilySearch
import os
import getpass
import re

load_dotenv()
if not os.environ.get("TAVILY_API_KEY"):
    os.environ["TAVILY_API_KEY"] = getpass.getpass("Tavily API key:\n")

TAVILY_API_KEY = os.getenv('TAVILY_API_KEY')

@tool("process_papers_content", return_direct=False)
def process_papers_content(url: str) -> str:
    """
    Processes content from a webpage and extracts structured sections 
    such as Title, Introduction, Methodology, Conclusion, etc.
    """

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except Exception as e:
        return f"Failed to fetch content from URL: {url} — Error: {e}"

    soup = BeautifulSoup(response.content, 'html.parser')
    text = soup.get_text(separator="\n")

    section_titles = [
        "Title", "Executive Summary", "Abstract", "Introduction", "Problem Statement",
        "Research Question", "Methodology", "Literature Review", "Background Work",
        "Main Body", "Analysis", "Findings", "Observations", "Discussion",
        "Conclusion", "Recommendations", "References", "Appendix"
    ]

    section_map = {title.lower(): title for title in section_titles}
    normalized_titles = [re.escape(title.lower()) for title in section_titles]

    extracted_sections = {}

    for section_key in normalized_titles:
        pattern = rf"(?i){section_key}\s*[:\-]?\s*\n?(.*?)(?=\n\n|\n({ '|'.join(normalized_titles) })|\Z)"
        match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
        if match:
            original_title = section_map[section_key]
            content = match.group(1).strip()
            if content:
                extracted_sections[original_title] = content[:2000]  # Optional: trim per section

    if extracted_sections:
        formatted_output = "\n\n".join(
            f"### {title}\n{content}" for title, content in extracted_sections.items()
        )
        return formatted_output
    return f"Unstructured Content Preview:\n\n{text[:2000]}"


@tool("process_content", return_direct=False)
def process_content(url: str) -> str:

    """Processes content from a webpage."""

    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup.get_text()


@tool("internet_search_DDGO", return_direct=False)
def internet_search_DDGO(query: str) -> str:

  """Searches the internet using DuckDuckGo."""

  with DDGS() as ddgs:
    results = [r for r in ddgs.text(query, max_results=5)]
    return results if results else "No results found."


@tool("internet_search_talvy", return_direct=False)
def internet_search_talvy(query: str) -> dict:
    """Searches the internet using Tavily and returns structured results."""
    search_tool = TavilySearch(api_key=TAVILY_API_KEY, max_results=5)
    results = search_tool.invoke(query)

    # Log the raw results for debugging purposes
    # print("Raw results:", results)

    if (isinstance(results, dict) and "results" in results and isinstance(results["results"], list) and all(isinstance(item, dict) for item in results["results"])
    ):
        return results
    else:
        return {
            "query": query,
            "error": "Unexpected result format. Please check the Tavily API response structure."
        }

def get_tools():
    # return [internet_search]   # Uncomment this and comment the line below to use Tavily instead of DuckDuckGo Search. 
    return [internet_search_DDGO, internet_search_talvy, process_content, process_papers_content]  # Uncomment this and comment the line above to use DuckDuckGo Search instead of Tavily.