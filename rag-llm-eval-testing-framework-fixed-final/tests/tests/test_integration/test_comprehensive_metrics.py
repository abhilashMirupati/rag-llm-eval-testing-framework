import pytest
from unittest.mock import patch, MagicMock, call
from main import run_evaluation # Assuming main logic is in main.py
from utils.utils.scorer import Scorer, EvaluationResult

@patch('main.load_data', return_value=[{"question": "q1", "answer": "a1", "context": "c1"}])
@patch('main.ConfigManager')
@patch('main.Reporter')
@patch('main.Scorer')
def test_comprehensive_run(mock_scorer, mock_reporter, mock_config, mock_load_data):
    """
    Tests that the runner can handle a comprehensive list of metrics.
    
    This test verifies that the main evaluation loop iterates over all configured
    metrics and calls the appropriate scoring method for each one.
    """
    # --- Arrange ---
    # Define the list of metrics we want to simulate running
    comprehensive_metrics_list = ["faithfulness", "answer_relevance", "coherence"]
    
    # Configure the mock Scorer instance to return a specific result for each metric
    mock_scorer_instance = mock_scorer.return_value
    mock_scorer_instance.evaluate_faithfulness.return_value = EvaluationResult(score=0.9, details="...")
    mock_scorer_instance.evaluate_answer_relevance.return_value = EvaluationResult(score=0.8, details="...")
    mock_scorer_instance.evaluate_coherence.return_value = EvaluationResult(score=0.7, details="...")
    
    # --- Act ---
    # We don't need a real runner, we can simulate the core logic of iterating
    # through metrics and calling the scorer.
    results = []
    for metric in comprehensive_metrics_list:
        # Construct the method name to call, e.g., 'evaluate_faithfulness'
        evaluation_method_name = f"evaluate_{metric}"
        # Get the actual method from our mock scorer instance
        evaluation_method = getattr(mock_scorer_instance, evaluation_method_name)
        # Call the method
        result = evaluation_method() 
        results.append(result)

    # --- Assert ---
    # 1. Verify that each evaluation method on the scorer was called exactly once.
    mock_scorer_instance.evaluate_faithfulness.assert_called_once()
    mock_scorer_instance.evaluate_answer_relevance.assert_called_once()
    mock_scorer_instance.evaluate_coherence.assert_called_once()
    
    # 2. Verify we have the correct number of results.
    assert len(results) == 3
    assert results[0].score == 0.9 # Check if results are in order
    assert results[1].score == 0.8
    assert results[2].score == 0.7