from typing import List, Dict, Any
from .scorer import Scorer, EvaluationResult
from .config_manager import ConfigManager
from .logger import setup_logger

logger = setup_logger(__name__)

class MetricsManager:
    """Orchestrates the evaluation of multiple metrics."""
    def __init__(self, scorer: Scorer, config_manager: ConfigManager):
        self.scorer = scorer
        self.config_manager = config_manager

    def evaluate_metrics(self, data_point: Dict[str, Any]) -> List[EvaluationResult]:
        results = []
        metrics_to_run = self.config_manager.get_metrics()
        for metric_name in metrics_to_run:
            evaluation_method_name = f"evaluate_{metric_name}"
            if not hasattr(self.scorer, evaluation_method_name):
                logger.warning(f"Metric '{metric_name}' is configured but no method found in Scorer. Skipping.")
                continue
            evaluation_method = getattr(self.scorer, evaluation_method_name)
            try:
                # This is a simplified example of argument mapping
                if metric_name in ["answer_relevance", "completeness", "helpfulness"]:
                    result = evaluation_method(answer=data_point["answer"], question=data_point["question"])
                elif metric_name in ["faithfulness", "factuality", "hallucination", "groundedness"]:
                    result = evaluation_method(answer=data_point["answer"], context=data_point["context"])
                elif metric_name in ["coherence", "conciseness", "fluency", "redundancy"]:
                    result = evaluation_method(answer=data_point["answer"])
                else:
                    result = evaluation_method(question=data_point["question"], answer=data_point["answer"], context=data_point["context"])
                results.append(result)
            except KeyError as e:
                logger.error(f"Missing key '{e}' in data point for metric '{metric_name}'. Skipping.")
            except Exception as e:
                logger.error(f"Error during evaluation of metric '{metric_name}': {e}")
        return results