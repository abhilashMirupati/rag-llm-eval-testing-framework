import pytest
from unittest.mock import patch, MagicMock
from main import run_evaluation # Assuming main logic is in main.py
from utils.utils.scorer import EvaluationResult

def custom_metric_function(answer: str, context: str) -> EvaluationResult:
    """
    This is a dummy custom metric function that we can use for testing.
    It simulates a user-defined evaluation.
    """
    return EvaluationResult(score=1.0, details="Custom metric executed successfully!")

@patch('main.load_data', return_value=[{"question": "q1", "answer": "a1", "context": "c1"}])
@patch('main.ConfigManager')
@patch('main.Reporter')
@patch('main.MetricsManager')
def test_custom_metric_execution(mock_metrics_manager, mock_reporter, mock_config, mock_load_data):
    """
    Tests if the framework can successfully run a custom metric.
    
    This test ensures that if a 'custom' metric is defined, the evaluation
    runner correctly identifies it and calls the appropriate execution logic.
    """
    # --- Arrange ---
    # Tell the mock MetricsManager to use our dummy custom function
    # when it encounters the "custom_metric_name".
    mock_metrics_instance = mock_metrics_manager.return_value
    mock_metrics_instance.evaluate_metrics.return_value = [
        custom_metric_function("a1", "c1")
    ]

    # Configure the mock ConfigManager to include our custom metric
    mock_config_instance = mock_config.return_value
    mock_config_instance.get_metrics.return_value = ["custom_metric_name"]
    mock_config_instance.get_reporter_config.return_value = {"report_formats": ["json"]}

    # --- Act ---
    run_evaluation(
        data_path="dummy_data.csv",
        config_path="dummy_config.json",
        output_dir="dummy_output",
        metrics=["custom_metric_name"]
    )

    # --- Assert ---
    # Verify that the metrics manager was asked to evaluate our list of metrics
    mock_metrics_instance.evaluate_metrics.assert_called_once()
    
    # Verify that the reporter received the result from our custom metric
    mock_reporter_instance = mock_reporter.return_value
    mock_reporter_instance.generate_report.assert_called_once()
    
    # Check the actual data passed to the reporter's generate_report method
    call_args, _ = mock_reporter_instance.generate_report.call_args
    reported_results = call_args[0]
    
    assert len(reported_results) == 1
    assert reported_results[0].score == 1.0
    assert reported_results[0].details == "Custom metric executed successfully!"
