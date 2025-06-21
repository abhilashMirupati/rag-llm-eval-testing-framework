import pytest
from typing import Dict, Any, List
from utils.utils.cli_formatter import CLIFormatter

@pytest.fixture
def sample_evaluation_results() -> List[Dict[str, Any]]:
    """
    Provides a sample list of evaluation results as a pytest fixture.
    """
    return [
        {
            "metric": "faithfulness",
            "score": 0.85,
            "details": "The model's answer was faithful to the context.",
            "passed": True,
        },
        {
            "metric": "answer_relevance",
            "score": 0.92,
            "details": "The answer was highly relevant to the question.",
            "passed": True,
        },
        {
            "metric": "context_precision",
            "score": 0.65,
            "details": "Some parts of the context were not relevant.",
            "passed": False,
        },
    ]

@pytest.fixture
def sample_summary_data() -> Dict[str, Any]:
    """
    Provides sample summary data as a pytest fixture.
    """
    return {
        "total_passed": 2,
        "total_failed": 1,
        "pass_rate": 66.67,
        "average_score": 0.81,
    }

def test_format_results(sample_evaluation_results: List[Dict[str, Any]]):
    """
    Tests the format_results function to ensure it formats individual
    metric results correctly.
    """
    formatted_output = CLIFormatter.format_results(sample_evaluation_results)

    assert "faithfulness" in formatted_output
    assert "0.85" in formatted_output
    assert "[PASSED]" in formatted_output
    assert "context_precision" in formatted_output
    assert "0.65" in formatted_output
    assert "[FAILED]" in formatted_output
    assert "The model's answer was faithful to the context." in formatted_output

def test_format_summary(sample_summary_data: Dict[str, Any]):
    """
    Tests the format_summary function to ensure it formats the
    summary section correctly.
    """
    formatted_output = CLIFormatter.format_summary(sample_summary_data)

    assert "Evaluation Summary" in formatted_output
    assert "Total Passed: 2" in formatted_output
    assert "Total Failed: 1" in formatted_output
    assert "Pass Rate: 66.67%" in formatted_output
    assert "Average Score: 0.81" in formatted_output

def test_empty_results_handling():
    """
    Tests that the formatter handles an empty list of results gracefully.
    """
    formatted_output = CLIFormatter.format_results([])
    assert formatted_output == ""

def test_empty_summary_handling():
    """
    Tests that the formatter handles empty or zero-value summary data.
    """
    empty_summary = {
        "total_passed": 0,
        "total_failed": 0,
        "pass_rate": 0.0,
        "average_score": 0.0,
    }
    formatted_output = CLIFormatter.format_summary(empty_summary)
    assert "Total Passed: 0" in formatted_output
    assert "Total Failed: 0" in formatted_output
    assert "Pass Rate: 0.00%" in formatted_output
    assert "Average Score: 0.00" in formatted_output
