# utils/research_classifier.py
from backend.logger.logger import CustomLogger

logger = CustomLogger().get_logger()


class ResearchClassifierTool:
    def __init__(self, llm, prompt):
        self.llm = llm
        self.prompt = prompt

        if not hasattr(self.llm, "invoke") and hasattr(self.llm, "__call__"):
            self.invoke_method = self.llm  # call directly
        else:
            self.invoke_method = self.llm.invoke  # use invoke method
    
    def research_classifier_run(self, state):
        """
        Run the LLM with the classification prompt and return updated state.
        """
        messages = state.get("messages")
        if not messages or not isinstance(messages, list):
            logger.error("State missing 'messages' or it's empty/invalid.")
            raise ValueError("Invalid state: 'messages' must be a non-empty list.")
        
        last_message = messages[-1]
        query = getattr(last_message, "content", None)
        if not query:
            logger.error("Last message missing 'content' attribute.")
            raise ValueError("Invalid message format: expected 'content' attribute.")

        input_messages = self.prompt.format_messages(query=query)
        response = self.invoke_method(input_messages)
        print(f"LLM raw response: {response}")
        logger.debug(f"LLM raw response: {response}")

        # Append response to state messages
        state["messages"] = messages + [response]
        logger.debug(f"Returning updated state with classifier response.")

        return state
        
    def route_decision_extraction_validation(self, state):
        messages = state.get("messages", [])
        if not messages:
            logger.warning("No messages in state for routing decision; defaulting to 'unknown'.")
            return "unknown"

        last_msg = messages[-1]
        if hasattr(last_msg, "content"):
            text = last_msg.content.strip().lower()
        else:
            text = str(last_msg).strip().lower()

        valid_labels = {"preprint", "biomedical", "multidisciplinary"}
        if text in valid_labels:
            return text
        else:
            logger.warning(f"LLM returned unknown label '{text}'. Defaulting to 'unknown'.")
            return "unknown"