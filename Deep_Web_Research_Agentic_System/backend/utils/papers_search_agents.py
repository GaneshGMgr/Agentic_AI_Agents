import os
import requests
from xml.etree import ElementTree as ET
from scholarly import scholarly
from dotenv import load_dotenv
from typing import List, Dict, Callable, Optional

load_dotenv()

SCIENCEDIRECT_API_KEY = os.getenv("ScienceDirect_Elsevier_API")
SPRINGER_API_KEY = os.getenv("Springer_API_Key")


def expand_with_related_topics(
    query: str,
    fetch_function: Callable[[str], List[Dict]],
    search_agent: Optional[object] = None,
    max_results: int = 5,
) -> List[Dict]:
    """Fetch papers for a query, then augment with papers on related topics suggested by an LLM agent."""
    papers = fetch_function(query)
    if len(papers) >= max_results or not search_agent:
        return papers[:max_results]

    try:
        response = search_agent.generate_reply(
            messages=[{"role": "user", "content": f"Suggest 3 related research topics for '{query}'"}]
        )
        related_topics = response.get("content", "").split("\n")
    except Exception as e:
        print("LLM related topics generation failed:", e)
        related_topics = []

    for topic in map(str.strip, related_topics):
        if topic and len(papers) < max_results:
            try:
                papers.extend(fetch_function(topic))
            except Exception as e:
                print(f"Fetching papers for related topic '{topic}' failed:", e)

    return papers[:max_results]

# --- Preprint / Early Stage ---

def fetch_arxiv_papers(query: str) -> List[Dict]:
    try:
        url = f"http://export.arxiv.org/api/query?search_query=all:{query}&start=0&max_results=5"
        response = requests.get(url)
        response.raise_for_status()
        root = ET.fromstring(response.text)
        return [{
            "title": entry.find("{http://www.w3.org/2005/Atom}title").text,
            "summary": entry.find("{http://www.w3.org/2005/Atom}summary").text,
            "link": entry.find("{http://www.w3.org/2005/Atom}id").text
        } for entry in root.findall("{http://www.w3.org/2005/Atom}entry")]
    except Exception as e:
        print("ArXiv API request failed:", e)
        return []


# --- Multidisciplinary ---

def fetch_google_scholar_papers(query: str) -> List[Dict]:
    try:
        results = scholarly.search_pubs(query)
        return [{
            "title": paper["bib"]["title"],
            "summary": paper["bib"].get("abstract", "No summary available"),
            "link": paper.get("pub_url", "No link available")
        } for _, paper in zip(range(5), results)]
    except Exception as e:
        print("Google Scholar error:", e)
        return []


def fetch_sciencedirect_papers(query: str) -> List[Dict]:
    if not SCIENCEDIRECT_API_KEY:
        print("ScienceDirect API key missing")
        return []
    try:
        headers = {"X-ELS-APIKey": SCIENCEDIRECT_API_KEY, "Accept": "application/json"}
        params = {"query": query, "count": 5, "sort": "relevance"}
        url = "https://api.elsevier.com/content/search/sciencedirect"
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        entries = response.json().get("search-results", {}).get("entry", [])
        return [{
            "title": entry.get("dc:title", "No title"),
            "summary": entry.get("dc:description", "No summary available"),
            "link": entry.get("prism:url", "No link available")
        } for entry in entries]
    except Exception as e:
        print("ScienceDirect API request failed:", e)
        return []


def fetch_semantic_scholar_papers(query: str) -> List[Dict]:
    try:
        url = "https://api.semanticscholar.org/graph/v1/paper/search"
        params = {"query": query, "limit": 5, "fields": "title,abstract,url"}
        response = requests.get(url, params=params)
        response.raise_for_status()
        return [{
            "title": paper.get("title", "No title"),
            "summary": paper.get("abstract", "No summary available"),
            "link": paper.get("url", "No link available")
        } for paper in response.json().get("data", [])]
    except Exception as e:
        print("Semantic Scholar API request failed:", e)
        return []


# --- Biomedical ---

def fetch_pubmed_papers(query: str) -> List[Dict]:
    try:
        base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
        search_url = f"{base_url}esearch.fcgi"
        fetch_url = f"{base_url}efetch.fcgi"
        params = {"db": "pubmed", "term": query, "retmode": "xml", "retmax": 5}

        search_response = requests.get(search_url, params=params)
        search_response.raise_for_status()
        ids = [id_elem.text for id_elem in ET.fromstring(search_response.text).findall(".//Id")]
        if not ids:
            return []

        fetch_response = requests.get(fetch_url, params={"db": "pubmed", "id": ",".join(ids), "retmode": "xml"})
        fetch_response.raise_for_status()

        root = ET.fromstring(fetch_response.text)
        return [{
            "title": article.find(".//ArticleTitle").text if article.find(".//ArticleTitle") is not None else "No title",
            "summary": article.find(".//AbstractText").text if article.find(".//AbstractText") is not None else "No abstract available",
            "link": f"https://pubmed.ncbi.nlm.nih.gov/{article.find('.//PMID').text}/" if article.find(".//PMID") is not None else "No link"
        } for article in root.findall(".//PubmedArticle")]
    except Exception as e:
        print("PubMed fetch failed:", e)
        return []


def fetch_springer_papers(query: str) -> List[Dict]:
    if not SPRINGER_API_KEY:
        print("Springer API key missing")
        return []
    try:
        url = "https://api.springernature.com/openaccess/jats"
        params = {"q": query, "api_key": SPRINGER_API_KEY, "p": 5}
        response = requests.get(url, params=params)
        response.raise_for_status()

        return [{
            "title": record.get("title", "No title"),
            "summary": record.get("abstract", "No abstract available"),
            "link": record.get("url", [{"value": "No link"}])[0]["value"]
        } for record in response.json().get("records", [])]
    except Exception as e:
        print("Springer API request failed:", e)
        return []