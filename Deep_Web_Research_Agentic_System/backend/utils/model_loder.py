import os
from dotenv import load_dotenv
from typing import Literal
from pydantic import BaseModel, Field

from backend.utils.config_loader import load_config  # YAML loader
from backend.logger.logger import CustomLogger
from backend.exception.exception import CustomException

from langchain_groq import ChatGroq
from langchain_ollama import OllamaLLM

load_dotenv()

# Initialize logger
logger = CustomLogger().get_logger()

class ConfigLoader:
    def __init__(self):
        try:
            logger.info("Loading config...")
            self.config = load_config()
        except Exception as e:
            logger.error(f"Failed to load config: {e}")
            raise CustomException("Error loading configuration") from e

    def __getitem__(self, key):
        try:
            return self.config[key]
        except KeyError as e:
            logger.error(f"Key '{key}' not found in config: {e}")
            raise CustomException(f"Config key '{key}' not found") from e


class ModelLoader(BaseModel):
    model_key: Literal[
        "groq", 
        "ollama-deepseek", 
        "ollama-llama3", 
        "ollama-mistral"
    ] = "ollama-llama3"

    config: ConfigLoader = Field(default_factory=ConfigLoader, exclude=True)

    class Config:
        arbitrary_types_allowed = True

    def load_llm(self):
        try:
            logger.info("LLM loading started...")
            logger.info(f"Loading model with config key: {self.model_key}")

            provider = self.config["llm"][self.model_key]["provider"]
            model_name = self.config["llm"][self.model_key]["model_name"]

            if provider == "groq":
                groq_api_key = os.getenv("GROQ_API_KEY")
                if not groq_api_key:
                    raise CustomException("GROQ_API_KEY is not set in environment.")
                logger.info(f"Using Groq model: {model_name}")
                return ChatGroq(model=model_name, api_key=groq_api_key)

            elif provider == "ollama":
                logger.info(f"Using Ollama model: {model_name}")
                return OllamaLLM(model=model_name)

            else:
                logger.error(f"Unsupported provider specified: {provider}")
                raise CustomException(f"Unsupported provider: {provider}")

        except Exception as e:
            logger.error(f"Failed to load LLM model: {e}")
            raise CustomException("Failed to initialize LLM") from e
