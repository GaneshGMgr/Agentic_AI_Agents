# research_classifier_tool.py
from backend.utils.research_classifier import ResearchClassifierTool
from langchain_core.messages import AIMessage

class ResearchClassifierAgent:
    def __init__(self, llm, prompt):
        self.classifier_tool = ResearchClassifierTool(llm, prompt)

    def run(self, state):
        """
        Calls the classifier tool to get the domain classification.
        Appends the response to the message list.
        """
        new_state = self.classifier_tool.research_classifier_run(state)
        label = self.classifier_tool.route_decision_extraction_validation(new_state)
        # Append route_label as a message:
        new_state["messages"].append(AIMessage(content=f"route_label: {label}"))
        print(f"[QueryClassifierAgent] route_label set to: {label}")
        return new_state

    def route_decision(self, state):
        """
        Reads the last message (the predicted label) and returns the node to route to.
        """
        label = self.classifier_tool.route_decision(state)
        route_map = {
            "preprint": "preprint_agent",
            "biomedical": "biomedical_agent",
            "multidisciplinary": "multidisciplinary_agent",
        }
        return route_map.get(label, "unknown_handler")
    
    def route_decision(self, state):
        messages = state.get("messages", [])
        for msg in reversed(messages):
            if hasattr(msg, "content") and msg.content.startswith("route_label:"):
                return msg.content.split(":", 1)[1].strip()
        return "unknown"