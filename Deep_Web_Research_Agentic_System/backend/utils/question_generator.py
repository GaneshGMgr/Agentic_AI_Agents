class QuestionGeneratorTool:
    def __init__(self, llm, prompt):
        self.llm = llm
        self.prompt = prompt

    def question_generator_run(self, user_input: str) -> str:
        input_messages = self.prompt.format_messages(user_input=user_input)
        response = self.llm.invoke(input_messages)
        return response["content"] if isinstance(response, dict) else str(response)

    # def route_decision(self, state):
    #     return state["messages"][-1]["content"].strip().lower()