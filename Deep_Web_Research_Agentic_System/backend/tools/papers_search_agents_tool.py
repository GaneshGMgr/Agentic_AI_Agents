from typing import List, Dict, Callable
from langchain_core.tools import tool
from pydantic import BaseModel, Field
from backend.utils.papers_search_agents import (
    expand_with_related_topics,
    fetch_arxiv_papers,
    fetch_google_scholar_papers,
    fetch_sciencedirect_papers,
    fetch_semantic_scholar_papers,
    fetch_pubmed_papers,
    fetch_springer_papers,
)

class Paper(BaseModel):
    title: str
    summary: str
    link: str

class PreprintAgentOutput(BaseModel):
    messages: List[Dict[str, str]]
    papers: List[Paper]

def make_search_preprint_papers_tool(llm) -> Callable:
    class InputModel(BaseModel):
        query: str

    @tool(
        "search_preprint_papers",
        args_schema=InputModel,
        return_direct=False,
        description="Search for preprint research papers on ArXiv based on the query."
    )
    def _search_preprint_papers(query: str) -> dict:
        papers = expand_with_related_topics(query, fetch_arxiv_papers, search_agent=llm)

        output = {
            "messages": [{"role": "system", "content": f"Found {len(papers)} preprint papers."}],
            "papers": papers
        }

        validated_output = PreprintAgentOutput(**output)
        return validated_output.model_dump()

    def wrapped_tool(input_state: dict) -> dict: # Wrapping the tool to extract only what's needed from the LangGraph state
        query = input_state.get("query")
        if not query:
            raise ValueError("Missing 'query' in LangGraph state")
        return _search_preprint_papers.invoke({"query": query})

    return wrapped_tool


# === Multidisciplinary Tool (Matching Structure) ===
def make_search_multidisciplinary_papers_tool(llm) -> Callable:
    class InputModel(BaseModel):
        query: str

    @tool(
        "search_multidisciplinary_papers",
        args_schema=InputModel,
        return_direct=False,
        description="Search multidisciplinary research papers from Google Scholar, ScienceDirect, and Semantic Scholar."
    )
    def _search_multidisciplinary_papers(query: str) -> dict:
        papers = []
        for fetcher in [
            fetch_google_scholar_papers,
            fetch_sciencedirect_papers,
            fetch_semantic_scholar_papers,
        ]:
            papers.extend(expand_with_related_topics(query, fetcher, search_agent=llm))
        papers = papers[:5]
        output = {
            "messages": [{"role": "system", "content": f"Found {len(papers)} multidisciplinary papers."}],
            "papers": papers
        }
        validated_output = PreprintAgentOutput(**output)
        return validated_output.model_dump()

    def wrapped_tool(input_state: dict) -> dict:
        query = input_state.get("query")
        if not query:
            raise ValueError("Missing 'query' in LangGraph state")
        return _search_multidisciplinary_papers.invoke({"query": query})

    return wrapped_tool


# === Biomedical Tool (Matching Structure) ===
def make_search_biomedical_papers_tool(llm) -> Callable:
    class InputModel(BaseModel):
        query: str

    @tool(
        "search_biomedical_papers",
        args_schema=InputModel,
        return_direct=False,
        description="Search biomedical research papers from PubMed and Springer."
    )
    def _search_biomedical_papers(query: str) -> dict:
        papers = []
        for fetcher in [fetch_pubmed_papers, fetch_springer_papers]:
            papers.extend(expand_with_related_topics(query, fetcher, search_agent=llm))
        papers = papers[:5]
        output = {
            "messages": [{"role": "system", "content": f"Found {len(papers)} biomedical papers."}],
            "papers": papers
        }
        validated_output = PreprintAgentOutput(**output)
        return validated_output.model_dump()

    def wrapped_tool(input_state: dict) -> dict:
        query = input_state.get("query")
        if not query:
            raise ValueError("Missing 'query' in LangGraph state")
        return _search_biomedical_papers.invoke({"query": query})

    return wrapped_tool