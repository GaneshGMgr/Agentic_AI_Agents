import os
import yaml
from pathlib import Path
from backend.logger.logger import CustomLogger
from backend.exception.exception import CustomException

logger = CustomLogger().get_logger()

def load_config(config_path: str = None) -> dict:
    if config_path is None:
        config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "config", "config.yaml"))
    
    try:
        with open(config_path, "r") as f:
            return yaml.safe_load(f)
    except Exception as e:
        logger.error(f"Failed to load config from {config_path}: {e}")
        raise CustomException(f"Error reading config file at {config_path}") from e
