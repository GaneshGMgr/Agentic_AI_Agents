import re
from typing import List
from backend.utils.internet_search import process_papers_content
from langchain_core.messages import AIMessage

class ReportWrittingAgent:
    def __init__(self, llm, prompt):
        self.llm = llm
        self.prompt = prompt  # should be a ChatPromptTemplate

    @staticmethod
    def _extract_urls(text: str) -> List[str]:
        pattern = r"https?://[^\s\]\)]+"  # Regex for URLs
        return re.findall(pattern, text)

    def run(self, state: dict) -> dict:
        papers = state.get("papers", [])
        query = state.get("query", "No original query provided.")
        print("Orginal Query for [ReportWrittingAgent]: ", query)

        if not papers:
            state.setdefault("messages", []).append({
                "role": "system",
                "content": "No papers found to write report."
            })
            return state

        all_urls = []
        # Enrich papers with scraped content from URLs
        for paper in papers:
            urls = self._extract_urls(str(paper))
            all_urls.extend(urls)
            contents = []
            for url in urls:
                try:
                    text = process_papers_content.invoke(url)
                    contents.append(f"Content from {url}:\n{text[:2000]}")  # limit to 2k chars
                except Exception as e:
                    contents.append(f"Could not fetch content from {url} (error: {e})")
            paper['paper_scrap'] = "\n\n".join(contents)
            print("Extracted Contents from papers for [ReportWrittingAgent]: ", contents)

        paper_summaries = "\n\n".join(
            f"Title: {p.get('title', 'No Title')}\nSummary: {p.get('summary', 'No Summary')}\nPaper Scrap:\n{p.get('paper_scrap', '')}"
            for p in papers
        )

        full_prompt_messages = self.prompt.format_messages(query=query, assistant_output=paper_summaries)
        response = self.llm.invoke(full_prompt_messages)

        final_message = AIMessage(content=response.content if hasattr(response, "content") else str(response))

        state.setdefault("messages", []).append({
            "role": "assistant",
            "content": final_message.content
        })

        state["found_urls"] = all_urls
        return state