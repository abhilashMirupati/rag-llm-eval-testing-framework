import yaml
from pathlib import Path
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field

@dataclass
class MetricConfig:
    """
    A dataclass to hold the configuration for a single metric.
    """
    name: str
    required_inputs: List[str] = field(default_factory=list)

class MetricManager:
    """
    Manages loading and accessing metric configurations from the capabilities file.
    This class is implemented as a singleton to ensure a single source of truth.
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        """Creates a singleton instance of the MetricManager."""
        if not cls._instance:
            cls._instance = super(MetricManager, cls).__new__(cls)
        return cls._instance

    def __init__(self, config_path: str = "models/model_capabilities.yaml"):
        """
        Initializes the MetricManager.

        Args:
            config_path: Path to the model capabilities YAML file.
        """
        # The singleton pattern ensures this __init__ logic is run only once.
        if hasattr(self, '_initialized'):
            return
            
        self.config_path = Path(config_path)
        self.config = self._load_config()
        self.metrics = self._load_metrics()
        self._initialized = True

    def _load_config(self) -> Dict[str, Any]:
        """Loads the capabilities from the YAML file."""
        if not self.config_path.is_file():
            raise FileNotFoundError(f"Metric capabilities configuration file not found at: {self.config_path}")
        
        try:
            with self.config_path.open('r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except yaml.YAMLError as e:
            raise ValueError(f"Error parsing YAML file '{self.config_path}': {e}") from e

    def _load_metrics(self) -> Dict[str, MetricConfig]:
        """Parses the loaded config data into MetricConfig objects."""
        metrics_data = self.config.get("metrics", {})
        return {
            name: MetricConfig(name=name, **params)
            for name, params in metrics_data.items()
        }

    def get_metric(self, metric_name: str) -> Optional[MetricConfig]:
        """
        Retrieves the configuration for a specific metric.

        Args:
            metric_name: The name of the metric.

        Returns:
            A MetricConfig object, or None if the metric is not found.
        """
        return self.metrics.get(metric_name)

    def get_supported_metrics(self, model_name: str) -> List[str]:
        """
        Gets the list of metric names supported by a given model.

        Args:
            model_name: The name of the model.

        Returns:
            A list of supported metric names. Returns an empty list if the model is not found.
        """
        return self.config.get("models", {}).get(model_name, {}).get("supported_metrics", [])

    def is_metric_supported(self, metric_name: str, model_name: str) -> bool:
        """
        Checks if a specific metric is supported by a specific model.

        Args:
            metric_name: The name of the metric.
            model_name: The name of the model.

        Returns:
            True if the metric is supported, False otherwise.
        """
        supported_metrics = self.get_supported_metrics(model_name)
        return metric_name in supported_metrics

# Create a global singleton instance for easy access across the application
metric_manager = MetricManager()
