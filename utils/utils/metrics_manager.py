import importlib
import logging

from utils.utils.config_manager import ConfigManager

class MetricsManager:
    """
    Manages the loading, initialization, and orchestration of evaluation metrics.
    Supports dynamic loading of both built-in and custom metrics via config.
    """
    def __init__(self, config):
        self.logger = logging.getLogger("metrics_manager")
        self.config = config
        self.metrics = self._load_metrics()

    def _load_metrics(self):
        """
        Loads and initializes metric classes based on the provided config.
        Returns a dict of metric_name: metric_instance.
        """
        metrics = {}
        metric_configs = self.config.get("metrics", [])
        if not metric_configs:
            self.logger.warning("No metrics specified in config. No evaluation will be performed.")
            return metrics

        for metric_entry in metric_configs:
            if isinstance(metric_entry, dict):
                # Support for metrics with config (name + params)
                metric_name = metric_entry.get("name")
                metric_params = metric_entry.get("params", {})
            else:
                metric_name = metric_entry
                metric_params = {}

            try:
                module_path, class_name = self._resolve_metric_path(metric_name)
                metric_module = importlib.import_module(module_path)
                metric_class = getattr(metric_module, class_name)
                metrics[metric_name] = metric_class(**metric_params)
                self.logger.info(f"Loaded metric: {metric_name} ({module_path}.{class_name})")
            except (ImportError, AttributeError, TypeError) as e:
                self.logger.error(f"Failed to load metric '{metric_name}': {e}")

        return metrics

    def _resolve_metric_path(self, metric_name):
        """
        Resolves the import path and class name for a given metric.
        This supports both built-in and custom metrics.
        """
        metric_config = ConfigManager.get_metric_config(metric_name)
        module_path = metric_config["module"]
        class_name = metric_config["class"]
        return module_path, class_name

    def get_metrics(self):
        """Returns the dict of loaded metric instances."""
        return self.metrics

    def evaluate_all(self, test_case, parsed_answer):
        """
        Evaluates all enabled metrics on a test case.
        Returns a dict of metric_name: score.
        """
        results = {}
        for name, metric in self.metrics.items():
            try:
                results[name] = metric.evaluate(test_case, parsed_answer)
            except Exception as e:
                self.logger.error(f"Metric '{name}' evaluation failed: {e}")
                results[name] = None
        return results
