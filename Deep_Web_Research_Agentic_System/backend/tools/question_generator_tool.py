from langchain_core.messages import SystemMessage, HumanMessage
from backend.utils.question_generator import QuestionGeneratorTool

class QuestionDecomposerAgent:
    def __init__(self, llm, prompt):
        self.question_generator_tool = QuestionGeneratorTool(llm, prompt)

    def generate_research_questions(self, user_input: str) -> str:
        """Generate 5–10 thoughtful sub-questions to explore a research topic."""
        return self.question_generator_tool.question_generator_run(user_input)

    def run(self, state):
        print("Full messages state:", state["messages"])
        query = None
        for msg in reversed(state["messages"]): # Find the last HumanMessage to get the original query
            if isinstance(msg, HumanMessage):
                query = msg.content
                break
        
        if query is None:
            raise ValueError("No original user query found in messages.")

        sub_questions = self.generate_research_questions(query)
        # print("Original Queries: ", query)
        # print("Sub Queries: ", sub_questions)
        
        state["sub_questions"] = sub_questions
        state["query"] = sub_questions
        state["messages"] = state["messages"] + [SystemMessage(content=sub_questions)]
        return state

    def get_tools(self):
        return [self.generate_research_questions]