# google_search_agent_tool.py

import re
from typing import List

from langchain_core.messages import AIMessage, SystemMessage, HumanMessage
from backend.prompt_library.prompts import report_writing_prompt
from backend.utils.internet_search import (
    get_tools,
    process_content,
    internet_search_DDGO,
    internet_search_talvy,
)


class InternetSearchAgent:
    def __init__(self, llm, prompt):
        self.llm = llm
        self.tools = get_tools()
        self.prompt = prompt
        self.report_writing_prompt = report_writing_prompt

    def _extract_urls(self, text: str) -> List[str]:
        """Extract URLs from a string using regex."""
        pattern = r"https?://[^\s\]\)]+"
        return re.findall(pattern, text)

    def run(self, state: dict) -> dict:    
        messages = state.get("messages", [])
        if not messages:
            raise ValueError("Empty messages in state")
        
        # Find route label from messages content:
        route_label = None
        for msg in reversed(messages):
            if hasattr(msg, "content") and msg.content.startswith("route_label:"):
                route_label = msg.content.split(":", 1)[1].strip()
                break
    
        # Extract original query (HumanMessage) and sub-questions (SystemMessage)
        original_query = None
        sub_questions = None
    
        for msg in reversed(messages):
            if isinstance(msg, HumanMessage) and not msg.content.strip().lower().startswith("google_search") and original_query is None:
                original_query = msg.content
            if isinstance(msg, SystemMessage) and sub_questions is None:
                sub_questions = msg.content
    
        print(f"[InternetSearchAgent] route_label found: {route_label}")
        # print(f"[InternetSearchAgent] Original query: {original_query}")
        # print(f"[InternetSearchAgent] Sub-questions: {sub_questions}")
    
        if route_label == "google_search":
            print(f"[SearchAgent] DuckDuckGo search triggered for: {original_query}")
            search_results = internet_search_DDGO.invoke(original_query)
            urls = self._extract_urls(str(search_results))
            print(f"[SearchAgent] Found URLs: {urls}")
    
            if not urls:
                new_state = state.copy()
                new_state["messages"] = messages + [AIMessage(content="No relevant links found from the search.")]
                return new_state
    
            contents = []
            for url in urls:
                try:
                    text = process_content.invoke(url)
                    contents.append(f"Content from {url}:\n{text[:2000]}")
                except Exception as e:
                    contents.append(f"Could not fetch content from {url} (error: {e})")
    
            web_results_combined = "\n\n".join(contents)

            full_prompt_messages = self.prompt.format_messages(query=original_query, web_results_combined=web_results_combined)
            response = self.llm.invoke(full_prompt_messages)
    
            final_message = AIMessage(
                content=response.content if hasattr(response, "content") else str(response)
            )
            new_state = state.copy()
            new_state["messages"] = messages + [final_message]
            new_state["found_urls"] = urls
            # print("DuckDukeGo return answer from model: ", new_state)
            return new_state
    
        else:
            print(f"[SearchAgent] Tavily search triggered for original query and sub-questions individually")
            queries_to_search = [original_query]
            
            if sub_questions:
                sub_question_list = [q.strip() for q in sub_questions.split("\n") if q.strip()]
                queries_to_search.extend(sub_question_list)
            
            all_results = []
            all_urls = []
            
            for q in queries_to_search:
                print(f"[SearchAgent] Tavily searching for: {q}")
                try:
                    results = internet_search_talvy.invoke(q)
                    # print(f"[SearchAgent] internet_search_talvy response result: {results}")
            
                    if "results" in results:
                        raw_result_items = results["results"]
                        urls = [r["url"] for r in raw_result_items if isinstance(r, dict) and "url" in r]
                        # print(f"[SearchAgent] Found URLs for query '{q}': {urls}")
                        all_results.append(f"Results for query: {q}\n{results}")
                        all_urls.extend(urls)
                    else:
                        error_message = results.get("error", "Unknown error")
                        # print(f"[SearchAgent] No results for query '{q}': {error_message}")
                        all_results.append(f"Error searching for query '{q}': {error_message}")
                except Exception as e:
                    print(f"[SearchAgent] Error searching for query '{q}': {e}")
                    all_results.append(f"Error searching for query '{q}': {e}")
            
            # Deduplicate URLs
            all_urls = list(set(all_urls))
            print("All available urls: ", all_urls)
            
            # Process content from URLs
            contents = []
            for url in all_urls:
                try:
                    text = process_content.invoke(url)
                    contents.append(f"Content from {url}:\n{text[:2000]}")
                except Exception as e:
                    contents.append(f"Could not fetch content from {url} (error: {e})")
            
            assistant_output = "\n\n".join(contents)
            
            full_prompt_messages = self.report_writing_prompt.format_messages(
                query=original_query,
                assistant_output=assistant_output
            )
            
            response = self.llm.invoke(full_prompt_messages)
            
            final_message = AIMessage(
                content=response.content if hasattr(response, "content") else str(response)
            )
            
            new_state = state.copy()
            new_state["messages"] = messages + [final_message]
            new_state["found_urls"] = all_urls
            
            return new_state
            