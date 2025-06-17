import pytest
from models.models.metric_config import metric_manager, MetricConfig

# We use the globally available 'metric_manager' instance for all tests.

def test_get_existing_metric():
    """
    Tests that get_metric correctly retrieves the configuration for an existing metric.
    """
    # Arrange
    metric_name = "faithfulness"
    
    # Act
    config = metric_manager.get_metric(metric_name)
    
    # Assert
    assert config is not None, f"Configuration for metric '{metric_name}' should not be None."
    assert isinstance(config, MetricConfig), "Should return a MetricConfig object."
    assert config.name == metric_name
    assert "answer" in config.required_inputs
    assert "context" in config.required_inputs

def test_get_non_existent_metric():
    """
    Tests that get_metric returns None for a metric that does not exist.
    """
    # Arrange
    metric_name = "non_existent_metric"
    
    # Act
    config = metric_manager.get_metric(metric_name)
    
    # Assert
    assert config is None, f"Configuration for a non-existent metric '{metric_name}' should be None."

@pytest.mark.parametrize("metric_name, model_name, expected_support", [
    # A metric that is supported by the model
    ("faithfulness", "gpt-4", True),
    # A metric that is not supported by the model
    ("answer_relevancy", "claude-2", False),
    # A metric that doesn't exist at all
    ("non_existent_metric", "gpt-4", False),
    # A model that doesn't exist at all
    ("faithfulness", "non_existent_model", False),
])
def test_is_metric_supported(metric_name: str, model_name: str, expected_support: bool):
    """
    Tests the is_metric_supported method for various combinations of metrics and models.
    """
    # Act
    is_supported = metric_manager.is_metric_supported(metric_name, model_name)
    
    # Assert
    assert is_supported == expected_support

def test_get_supported_metrics_for_model():
    """
    Tests that get_supported_metrics returns the correct list of metrics for a given model.
    """
    # Arrange
    model_name = "gpt-4"
    
    # Act
    supported_metrics = metric_manager.get_supported_metrics(model_name)
    
    # Assert
    assert isinstance(supported_metrics, list), "Should return a list."
    assert "faithfulness" in supported_metrics
    assert "answer_relevancy" in supported_metrics
    # This metric is listed as not supported for gpt-4 in the YAML, so it should not be here.
    assert "context_relevancy" not in supported_metrics

def test_get_supported_metrics_for_non_existent_model():
    """
    Tests that get_supported_metrics returns an empty list for a model that does not exist.
    """
    # Arrange
    model_name = "non_existent_model"
    
    # Act
    supported_metrics = metric_manager.get_supported_metrics(model_name)
    
    # Assert
    assert supported_metrics == [], "Should return an empty list for a non-existent model."