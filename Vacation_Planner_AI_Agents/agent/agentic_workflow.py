
from utils.model_loader import ModelLoader
from prompt_library.prompt import SYSTEM_PROMPT
from langgraph.graph import StateGraph, MessagesState, END, START
from langgraph.prebuilt import ToolNode, tools_condition
from tools.weather_info_tool import WeatherInfoTool
from tools.place_search_tool import PlaceSearchTool
from tools.expense_calculator_tool import CalculatorTool
from tools.currency_conversion_tool import CurrencyConverterTool

class GraphBuilder():
    def __init__(self,model_provider: str = "ollama-llama3"): # default is "ollama"

        # here self.model_loader holds all the data and methods defined inside the ModelLoader class, including the method load_llm()
        self.model_loader = ModelLoader(model_key=model_provider)
        self.llm = self.model_loader.load_llm()
        
        self.tools = []
        
        self.weather_tools = WeatherInfoTool()
        self.place_search_tools = PlaceSearchTool()
        self.calculator_tools = CalculatorTool()
        self.currency_converter_tools = CurrencyConverterTool()
        
        self.tools.extend([* self.weather_tools.weather_tool_list, 
                           * self.place_search_tools.place_search_tool_list,
                           * self.calculator_tools.calculator_tool_list,
                           * self.currency_converter_tools.currency_converter_tool_list
                           ])
        
        # self.llm_with_tools = self.llm.bind_tools(tools=self.tools)
        self.llm_with_tools = self.llm 
        
        self.graph = None
        
        self.system_prompt = SYSTEM_PROMPT
    
    
    def agent_function(self,state: MessagesState):
        """Main agent function"""
        user_question = state["messages"]
        input_question = [self.system_prompt] + user_question
        # response = self.llm_with_tools.invoke(input_question)
        response = self.llm.invoke(input_question)
        return {"messages": [response]}
    def build_graph(self):
        graph_builder=StateGraph(MessagesState)
        graph_builder.add_node("agent", self.agent_function) # this will be agent function which decides which tool(s) to call
        graph_builder.add_node("tools", ToolNode(tools=self.tools)) # this is where the actual tool will be called, based on agent's decision
        graph_builder.add_edge(START,"agent") # starting point of graph: first go to "agent" node
        graph_builder.add_conditional_edges("agent",tools_condition) # From the "agent" node, decide next step based on condition (like which tool to use or finish)
        graph_builder.add_edge("tools","agent") # After calling a tool, return back to the agent to decide the next move
        graph_builder.add_edge("agent",END) # If the agent determines everything is done, move to the END state
        self.graph = graph_builder.compile() # Compile the whole graph into a runnable execution flow
        return self.graph
        
    def __call__(self): # __call__ method allows any object to behave like a function
        return self.build_graph()