# agentic_pipeline.py
from langgraph.graph import StateGraph, START, END
from backend.utils.model_loder import ModelLoader
from backend.tools.report_writting_agent import ReportWrittingAgent
from backend.tools.query_classifier_tool import QueryClassifierAgent
from backend.tools.internet_search_tool import InternetSearchAgent
from backend.tools.question_generator_tool import QuestionDecomposerAgent
from backend.tools.research_classifier_tool import ResearchClassifierAgent
from backend.tools.papers_search_agents_tool import (
    make_search_preprint_papers_tool,
    make_search_multidisciplinary_papers_tool,
    make_search_biomedical_papers_tool
)
from backend.prompt_library.prompts import (
    query_classifier_prompt,
    research_classifier_prompt,
    question_decomposition_prompt,
    internet_search_prompt,
    report_writing_prompt
)
from typing import TypedDict, List, Optional

class CustomState(TypedDict):
    messages: list
    found_urls: List[str]
    query: Optional[str]
    sub_questions: Optional[str]
    papers: Optional[List[dict]]

class GraphBuilder:
    def __init__(self, model_provider: str = "ollama-llama3", classifier_model: str = "ollama-llama3"):
        self.model_loader = ModelLoader(model_key=model_provider)
        self.classifier_loader = ModelLoader(model_key=classifier_model)

        self.llm = self.model_loader.load_llm()
        self.classifier_llm = self.classifier_loader.load_llm()

        self.query_classifier_agent = QueryClassifierAgent(
            llm=self.classifier_llm, prompt=query_classifier_prompt
        )

        self.research_classifier_agent = ResearchClassifierAgent(
            llm=self.classifier_llm, prompt=research_classifier_prompt
        )

        self.internet_search_agent = InternetSearchAgent(
            llm=self.llm, prompt=internet_search_prompt
        )
        self.question_decomposer = QuestionDecomposerAgent(
            llm=self.llm, prompt=question_decomposition_prompt
        )
        self.report_writting_agent = ReportWrittingAgent(
            llm=self.llm, prompt=report_writing_prompt
        )

        self.preprint_agent = make_search_preprint_papers_tool(self.llm)
        self.multidisciplinary_agent = make_search_multidisciplinary_papers_tool(self.llm)
        self.biomedical_agent = make_search_biomedical_papers_tool(self.llm)
        
    def build_graph(self):
        graph = StateGraph(CustomState)

        graph.add_node("query_classifier", self.query_classifier_agent.run) # run(state) i.e is run(query)
        graph.add_node("internet_search_agent", self.internet_search_agent.run) # run(query) or run(query + subquery) query_classifier report_generator
        graph.add_node("question_decomposer", self.question_decomposer.run) # run(query)
        graph.add_node("research_classifier_agent", self.research_classifier_agent.run)
        graph.add_node("report_writting_agent", self.report_writting_agent.run)
        graph.add_node("preprint_agent", self.preprint_agent)
        graph.add_node("biomedical_agent", self.biomedical_agent)
        graph.add_node("multidisciplinary_agent", self.multidisciplinary_agent)

        graph.add_edge(START, "query_classifier")

        graph.add_conditional_edges(
            "query_classifier",
            self.query_classifier_agent.route_decision,
            {
                "google_search": "internet_search_agent",
                "report_generation": "question_decomposer",
                "research_paper": "research_classifier_agent",
            },
        )

        graph.add_conditional_edges(
            "research_classifier_agent",
            self.research_classifier_agent.route_decision,
            {
                "preprint": "preprint_agent",
                "biomedical": "biomedical_agent",
                "multidisciplinary": "multidisciplinary_agent",
            },
        )

        graph.add_edge("question_decomposer", "internet_search_agent")
        graph.add_edge("internet_search_agent", END)
        graph.add_edge("preprint_agent", "report_writting_agent")
        graph.add_edge("biomedical_agent", "report_writting_agent")
        graph.add_edge("multidisciplinary_agent", "report_writting_agent")
        graph.add_edge("report_writting_agent", END)

        return graph.compile()

    def __call__(self):
        return self.build_graph()
