from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from agent.agentic_workflow import GraphBuilder
from utils.save_to_document import save_document
from starlette.responses import JSONResponse
from langchain_core.messages import HumanMessage
from utils.config_loader import load_config
import os
import datetime
import traceback
from dotenv import load_dotenv
from pydantic import BaseModel
load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,  # Enable CORS middleware to handle cross-origin requests
    allow_origins=["*"],  # Allow all domains (use specific domain in production)
    allow_credentials=True,  # Allow cookies, auth headers, etc.
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allow all custom headers (Content-Type, Authorization, etc.)
)

class QueryRequest(BaseModel):
    question: str
    model: str = "ollama-llama3"  # default model

@app.post("/query")
async def query_travel_agent(query:QueryRequest):
    try:
        print("user query: ", query.question)
        print("user selected model: ", query.model)
        # graph = GraphBuilder(model_provider="ollama-llama3") # default mode is ollama-llama3
        valid_models = load_config().get("llm", {})
        model_key = query.model if query.model in valid_models else "ollama-llama3"
        graph = GraphBuilder(model_provider=model_key)
        react_app=graph() # __call__ method allows any object to behave like a function
        #react_app = graph.build_graph() # # <- no need to create __call__() insider GraphBuilder()


        
        ## In LangGraph:
        # When we call compile() on a StateGraph, it returns a CompiledGraph object.
        # This CompiledGraph class comes with built-in methods, including:
        # get_graph() → returns the internal graph representation.
        # draw_mermaid() → shows a Mermaid.js diagram.
        # draw_mermaid_png() → returns a PNG image of the flowchart.
        png_graph = react_app.get_graph().draw_mermaid_png()
        with open("./media/my_graph.png", "wb") as f:
            f.write(png_graph)

        print(f"Graph saved as 'my_graph.png' in {os.getcwd()}")

        # Assuming request is a pydantic object like: {"question": "your text"}
        # messages={"messages": [query.question]} # validating with pydantic  QueryRequest
        messages = {"messages": [HumanMessage(content=query.question)]}
        print("Invoking graph with messages:", messages)
        output = react_app.invoke(messages)

        # Extract the final response
        final_output = (
            output["messages"][-1].content if isinstance(output, dict) and "messages" in output
            else str(output)
        )

        # Save the output to a Markdown file
        filename = save_document(final_output)

        return {
            "answer": final_output,
            "document": filename
        }
    except Exception as e:
        traceback.print_exc()
        return JSONResponse(status_code=500, content={"error": str(e)})