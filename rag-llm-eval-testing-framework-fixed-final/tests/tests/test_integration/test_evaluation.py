import pytest
from unittest.mock import patch, MagicMock
from main import run_evaluation # Assuming the main logic is in main.py
from utils.utils.scorer import EvaluationResult

@pytest.fixture
def mock_components():
    """
    A single fixture to patch all major components for integration testing.
    This keeps the test function signature clean.
    """
    with patch('main.ConfigManager') as mock_config, \
         patch('main.MetricsManager') as mock_metrics, \
         patch('main.Reporter') as mock_reporter, \
         patch('main.load_data') as mock_data:
        
        # --- Arrange ---
        # Configure the return values for all mocked components
        
        # Mock for load_data
        mock_data.return_value = [{"question": "q1", "answer": "a1", "context": "c1"}]
        
        # Mock for ConfigManager instance
        mock_config_instance = mock_config.return_value
        mock_config_instance.get_model_name.return_value = "mock-model"
        mock_config_instance.get_metrics.return_value = ["faithfulness"]
        mock_config_instance.get_reporter_config.return_value = {"report_formats": ["json"]}

        # Mock for MetricsManager instance
        mock_metrics_instance = mock_metrics.return_value
        mock_metrics_instance.evaluate_metrics.return_value = [
            EvaluationResult(score=0.9, details="Mocked faithfulness score")
        ]
        
        # Mock for Reporter instance
        mock_reporter_instance = mock_reporter.return_value

        yield {
            "load_data": mock_data,
            "ConfigManager": mock_config,
            "MetricsManager": mock_metrics,
            "Reporter": mock_reporter,
            "config_instance": mock_config_instance,
            "metrics_instance": mock_metrics_instance,
            "reporter_instance": mock_reporter_instance
        }

def test_full_evaluation_flow(mock_components: dict):
    """
    Tests the main end-to-end evaluation flow using mocked components.
    
    This test verifies that the main `run_evaluation` function correctly
    orchestrates the loading of data, configuration, evaluation, and reporting.
    """
    # --- Act ---
    # Run the main function with dummy arguments, since our mocks will intercept everything.
    run_evaluation(
        data_path="dummy_data.csv",
        config_path="dummy_config.json",
        output_dir="dummy_output",
        model_name="mock-model",
        metrics=["faithfulness"],
        report_formats=["json"]
    )

    # --- Assert ---
    # Verify that each component was used as expected.
    
    # 1. Was the data loaded?
    mock_components["load_data"].assert_called_once_with("dummy_data.csv")
    
    # 2. Was the configuration manager initialized?
    mock_components["ConfigManager"].assert_called_once_with("dummy_config.json")
    
    # 3. Was the metrics manager initialized and used?
    mock_components["MetricsManager"].assert_called_once()
    mock_components["metrics_instance"].evaluate_metrics.assert_called_once()
    
    # 4. Was the reporter initialized and used with the results from the metrics manager?
    mock_components["Reporter"].assert_called_once()
    results = mock_components["metrics_instance"].evaluate_metrics.return_value
    mock_components["reporter_instance"].generate_report.assert_called_once_with(
        results=results,
        report_formats=["json"]
    )