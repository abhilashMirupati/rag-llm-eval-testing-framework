import json
from pathlib import Path
from typing import Dict, Any, List, Optional

class ConfigManager:
    """Manages loading and accessing the framework's configuration."""

    def __init__(self, config_path: str = 'config.json'):
        self.config_path = Path(config_path)
        self.config = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        """Loads the configuration from the specified JSON file."""
        if not self.config_path.is_file():
            raise FileNotFoundError(f"Configuration file not found at: {self.config_path}")
        
        try:
            with self.config_path.open('r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(f"Error decoding JSON from config file: {self.config_path}") from e

    def get_model_name(self) -> str:
        return self.config.get("model_name", "gpt-4")

    def get_metrics(self) -> List[str]:
        return self.config.get("metrics", [])

    def get_llm_provider(self) -> str:
        return self.config.get("llm_provider", "openai")
        
    def get_reporter_config(self) -> Dict[str, Any]:
        return self.config.get("reporter", {})

    def get_data_loader_config(self) -> Dict[str, Any]:
        return self.config.get("data_loader", {})

    def get_api_key(self, provider: str) -> Optional[str]:
        return self.config.get("api_keys", {}).get(provider)