import yaml
from pathlib import Path
from typing import Dict, Any, List, Optional

class ModelManager:
    """
    Manages loading and accessing model capabilities from a YAML configuration file.
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        """Creates a singleton instance of the ModelManager."""
        if not cls._instance:
            cls._instance = super(ModelManager, cls).__new__(cls)
        return cls._instance

    def __init__(self, config_path: str = "models/model_capabilities.yaml"):
        """
        Initializes the ModelManager.

        Args:
            config_path: Path to the model capabilities YAML file.
        """
        # Ensure __init__ is only run once for the singleton instance
        if not hasattr(self, '_initialized'):
            self.config_path = Path(config_path)
            self.config = self._load_config()
            self._initialized = True

    def _load_config(self) -> Dict[str, Any]:
        """Loads the model capabilities from the YAML file."""
        if not self.config_path.is_file():
            raise FileNotFoundError(f"Model capabilities configuration file not found at: {self.config_path}")
        
        try:
            with self.config_path.open('r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except yaml.YAMLError as e:
            raise ValueError(f"Error parsing YAML file '{self.config_path}': {e}") from e

    def get_model_config(self, model_name: str) -> Optional[Dict[str, Any]]:
        """
        Retrieves the entire configuration for a specific model.

        Args:
            model_name: The name of the model.

        Returns:
            A dictionary containing the model's configuration, or None if not found.
        """
        return self.config.get("models", {}).get(model_name)

    def get_supported_metrics(self, model_name: str) -> List[str]:
        """
        Gets the list of metrics supported by a given model.

        Args:
            model_name: The name of the model.

        Returns:
            A list of supported metric names. Returns an empty list if the
            model is not found.
        """
        model_config = self.get_model_config(model_name)
        return model_config.get("supported_metrics", []) if model_config else []

# Create a global singleton instance for easy access across the application
model_manager = ModelManager()