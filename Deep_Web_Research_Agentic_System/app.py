# === app.py ===
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from langgraph.graph import MessagesState
from langchain_core.messages import HumanMessage
from backend.utils.save_to_documents import save_document

from dotenv import load_dotenv
import traceback
import os

from backend.exception.exception import CustomException
from backend.logger.logger import CustomLogger
from backend.agents.agentic_pipeline import GraphBuilder
from backend.utils.config_loader import load_config
from fastapi import APIRouter

load_dotenv()

app = FastAPI()
api_router = APIRouter()
logger = CustomLogger().get_logger()

# Define paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "frontend/statics")
INDEX_HTML_PATH = os.path.join(BASE_DIR, "frontend/templates/index.html")
GRAPH_IMAGE_PATH = os.path.join(STATIC_DIR, "media/graph_architecture.png")


app.add_middleware(
    CORSMiddleware,  # Enable CORS middleware to handle cross-origin requests
    allow_origins=["*"],  # Allow all domains (use specific domain in production)
    allow_credentials=True,  # Allow cookies, auth headers, etc.
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allow all custom headers (Content-Type, Authorization, etc.)
)

class SaveRequest(BaseModel):
    text: str

class QueryRequest(BaseModel):
    question: str
    model: str = "ollama-llama3"


# API Routes on router
@api_router.get("/models")
async def get_models():
    try:
        config = load_config()
        return config.get("llm", {})
    except Exception as e:
        logger.error(f"Error loading models: {str(e)}")
        return JSONResponse(status_code=500, content={"error": str(e)})


@api_router.post("/process-query")
async def query_travel_agent(query: QueryRequest):
    try:
        # logger.info(f"Received query: {query.question}")
        # logger.info(f"Selected model: {query.model}")

        valid_models = load_config().get("llm", {})
        model_key = query.model if query.model in valid_models else "ollama-llama3"
        if model_key == "auto":
            model_key = "ollama-llama3"

        model_name_used = valid_models.get(model_key, {}).get("model_name", "unknown")
        logger.info(f"Using model provider: {model_key} ({model_name_used})")

        print("Received query: ", model_key)
        graph = GraphBuilder(model_provider=model_key)
        compiled_graph = graph()

        # Initialize state with user question
        initial_state = MessagesState(messages=[HumanMessage(content=query.question)])

        # Run the graph pipeline
        final_state = compiled_graph.invoke(initial_state)

        answer = "No response generated."
        urls = []
        papers = []

        if final_state.get("messages"):
            ai_message = final_state["messages"][-1]
            answer = ai_message.get("content") if isinstance(ai_message, dict) else getattr(ai_message, "content", "No content")
            urls = final_state.get("found_urls", [])
            papers = final_state.get("papers", [])

        # Try saving the graph image for visualization
        try:
            png_graph = compiled_graph.get_graph().draw_mermaid_png()
            with open(GRAPH_IMAGE_PATH, "wb") as f:
                f.write(png_graph)
            logger.info(f"Graph saved as 'graph_architecture.png' in {GRAPH_IMAGE_PATH}")
        except Exception as e:
            logger.warning(f"Failed to save graph image: {e}")

        return JSONResponse(status_code=200, content={
            "answer": answer,
            # "papers": papers,  # Uncomment if you want to return papers as well
            "references": urls,
            "model_used": model_name_used
        })

    except CustomException as ce:
        logger.error(f"CustomException: {ce}\n{traceback.format_exc()}")
        return JSONResponse(status_code=400, content={"error": str(ce)})

    except Exception as e:
        logger.error(f"Unhandled Exception: {traceback.format_exc()}")
        return JSONResponse(status_code=500, content={"error": "Internal Server Error"})


@api_router.post("/save-document")
async def save_document_api(request: SaveRequest):
    try:
        logger.info("Saving document from API request")
        filename = save_document(request.text)
        logger.info(f"Document saved as {filename}")
        return {"message": f"Document saved as {filename}"}
    except CustomException as ce:
        logger.error(f"CustomException in save_document_api: {ce}\n{traceback.format_exc()}")
        return JSONResponse(status_code=400, content={"error": str(ce)})
    except Exception as e:
        logger.error(f"Unhandled exception in save_document_api: {traceback.format_exc()}")
        return JSONResponse(status_code=500, content={"error": "Internal Server Error"})


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/", include_in_schema=False)
async def root_redirect():
    return RedirectResponse(url="/index.html")


# Register API router under /api prefix
app.include_router(api_router, prefix="/api")

# Serve frontend static files from root /
app.mount("/statics", StaticFiles(directory=os.path.join(BASE_DIR, "frontend/statics")), name="statics")
app.mount("/", StaticFiles(directory=os.path.join(BASE_DIR, "frontend/templates"), html=True), name="frontend")

# === Command ===
# Run with: uvicorn app:app --reload --host 0.0.0.0 --port 8000
