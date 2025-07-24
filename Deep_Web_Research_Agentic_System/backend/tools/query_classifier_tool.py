from backend.utils.query_classifier import QueryClassifierTool
from langchain_core.messages import AIMessage

class QueryClassifierAgent:
    def __init__(self, llm, prompt):
        self.classifier_tool = QueryClassifierTool(llm, prompt)

    def run(self, state):
        new_state = self.classifier_tool.query_classifier_run(state)
        label = self.classifier_tool.route_decision_extraction_validation(new_state)
        
        # Append route_label as a message:
        new_state["messages"].append(AIMessage(content=f"route_label: {label}"))
        print(f"[QueryClassifierAgent] route_label set to: {label}")
        return new_state

    def route_decision(self, state):
        messages = state.get("messages", [])
        for msg in reversed(messages):
            if hasattr(msg, "content") and msg.content.startswith("route_label:"):
                return msg.content.split(":", 1)[1].strip()
        return "unknown"