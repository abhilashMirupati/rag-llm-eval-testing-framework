import pytest
from models.models.metric_config import metric_manager, MetricConfig

def test_get_existing_metric():
    """
    Tests that get_metric correctly retrieves the configuration for an existing metric.
    """
    metric_name = "faithfulness"
    config = metric_manager.get_metric(metric_name)
    assert config is not None, f"Configuration for metric '{metric_name}' should not be None."
    assert isinstance(config, MetricConfig), "Should return a MetricConfig object."
    assert config.name == metric_name
    assert "answer" in config.required_inputs
    assert "context" in config.required_inputs

def test_get_non_existent_metric():
    """
    Tests that get_metric returns None for a metric that does not exist.
    """
    metric_name = "non_existent_metric"
    config = metric_manager.get_metric(metric_name)
    assert config is None, f"Configuration for a non-existent metric '{metric_name}' should be None."

@pytest.mark.parametrize("metric_name, model_name, expected_support", [
    ("faithfulness", "gpt-4", True),
    ("answer_relevancy", "claude-2", False),
    ("non_existent_metric", "gpt-4", False),
    ("faithfulness", "non_existent_model", False),
])
def test_is_metric_supported(metric_name: str, model_name: str, expected_support: bool):
    is_supported = metric_manager.is_metric_supported(metric_name, model_name)
    assert is_supported == expected_support

def test_get_supported_metrics_for_model():
    model_name = "gpt-4"
    supported_metrics = metric_manager.get_supported_metrics(model_name)
    assert isinstance(supported_metrics, list), "Should return a list."
    assert "faithfulness" in supported_metrics
    assert "answer_relevancy" in supported_metrics
    assert "context_relevancy" not in supported_metrics

def test_get_supported_metrics_for_non_existent_model():
    model_name = "non_existent_model"
    supported_metrics = metric_manager.get_supported_metrics(model_name)
    assert supported_metrics == [], "Should return an empty list for a non-existent model."
