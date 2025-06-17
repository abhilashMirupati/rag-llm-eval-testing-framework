import pytest
from unittest.mock import patch, MagicMock
from main import run_evaluation  # Assuming 'run_evaluation' is the main entry point in your main.py
from utils.utils.scorer import EvaluationResult

# Mock data to be returned by the Scorer
MOCK_EVALUATION_RESULTS = [
    EvaluationResult(metric_name="faithfulness", score=0.9, details="Mock details for faithfulness"),
    EvaluationResult(metric_name="answer_relevance", score=0.8, details="Mock details for answer relevance"),
]

@patch('main.MetricsManager')
@patch('main.Reporter')
@patch('main.ConfigManager')
@patch('main.load_data')
def test_evaluation_runner_flow(
    mock_load_data: MagicMock,
    mock_config_manager: MagicMock,
    mock_reporter: MagicMock,
    mock_metrics_manager: MagicMock
):
    """
    Tests the main evaluation runner's end-to-end flow using mocks.

    This test patches the major components to verify that the runner:
    1. Loads data and configuration correctly.
    2. Initializes the MetricsManager with the right scorer.
    3. Calls the evaluation method.
    4. Passes the results to the Reporter.
    """
    # --- Arrange ---
    # Configure the return values of our mocks
    mock_load_data.return_value = [{"question": "q1", "answer": "a1", "context": "c1"}]
    
    # Mock for ConfigManager instance
    mock_config_instance = mock_config_manager.return_value
    mock_config_instance.get_model_name.return_value = "mock-gpt-4"
    mock_config_instance.get_metrics.return_value = ["faithfulness", "answer_relevance"]
    mock_config_instance.get_reporter_config.return_value = {"report_formats": ["json"]}
    
    # Mock for MetricsManager instance
    mock_metrics_manager_instance = mock_metrics_manager.return_value
    mock_metrics_manager_instance.evaluate_metrics.return_value = MOCK_EVALUATION_RESULTS
    
    # Mock for Reporter instance
    mock_reporter_instance = mock_reporter.return_value

    # --- Act ---
    # Run the main evaluation function with some mock arguments
    run_evaluation(
        data_path="dummy/path.csv",
        config_path="dummy/config.json",
        output_dir="dummy/output",
        model_name="mock-gpt-4",
        metrics=["faithfulness", "answer_relevance"],
        report_formats=["json"]
    )

    # --- Assert ---
    # Verify that the key methods were called as expected
    mock_load_data.assert_called_once_with("dummy/path.csv")
    mock_config_manager.assert_called_once_with("dummy/config.json")
    
    # Check that MetricsManager was initialized and used
    mock_metrics_manager.assert_called_once()
    mock_metrics_manager_instance.evaluate_metrics.assert_called_once()
    
    # Check that the results were passed to the Reporter
    mock_reporter.