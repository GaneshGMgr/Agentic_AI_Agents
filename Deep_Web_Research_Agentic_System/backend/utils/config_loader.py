import os
import yaml
from pathlib import Path

def load_config(config_path: str = None) -> dict:
    if config_path is None:
        config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "config", "config.yaml"))

    with open(config_path, "r") as f:
        return yaml.safe_load(f)