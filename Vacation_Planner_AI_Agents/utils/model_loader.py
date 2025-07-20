import os
from dotenv import load_dotenv
from typing import Literal
from pydantic import BaseModel, Field
from utils.config_loader import load_config # yaml loader
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from langchain_ollama import OllamaLLM

load_dotenv()

class ConfigLoader:
    def __init__(self):
        print("Loading config...")
        self.config = load_config()

    def __getitem__(self, key):
        return self.config[key]

class ModelLoader(BaseModel): # BaseModel helps with data validation, settings management, and more 
    # it can only be one of these exact strings: "groq", "openai", "ollama-deepseek", "ollama-llama3", or "ollama-mistral"
    # It acts like a validation check: if you try to create a ModelLoader instance with some other string as model_key, Pydantic will raise an error.
    model_key: Literal[
        "groq", 
        "openai", 
        "ollama-deepseek", 
        "ollama-llama3", 
        "ollama-mistral"
    ] = "ollama-llama3" # default is ollama-llama3

    config: ConfigLoader = Field(default_factory=ConfigLoader, exclude=True)

    class Config:
        arbitrary_types_allowed = True

    def load_llm(self):
        print("LLM loading...")
        print(f"Loading model with config key: {self.model_key}")

        # Read provider and model_name dynamically from config
        provider = self.config["llm"][self.model_key]["provider"]
        model_name = self.config["llm"][self.model_key]["model_name"]

        if provider == "groq":
            groq_api_key = os.getenv("GROQ_API_KEY")
            print(f"Using Groq model: {model_name}")
            return ChatGroq(model=model_name, api_key=groq_api_key)

        elif provider == "openai":
            openai_api_key = os.getenv("OPENAI_API_KEY")
            print(f"Using OpenAI model: {model_name}")
            return ChatOpenAI(model_name=model_name, api_key=openai_api_key)

        elif provider == "ollama":
            print(f"Using Ollama model: {model_name}")
            return OllamaLLM(model=model_name)

        else:
            raise ValueError(f"Unsupported provider: {provider}")