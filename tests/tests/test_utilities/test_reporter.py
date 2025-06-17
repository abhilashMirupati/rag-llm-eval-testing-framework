import pytest
from pathlib import Path
from typing import List, Dict, Any
from utils.utils.reporter import Reporter
from utils.utils.scorer import EvaluationResult

@pytest.fixture
def sample_evaluation_results_for_report() -> List[EvaluationResult]:
    """
    Provides a sample list of EvaluationResult objects for testing the reporter.
    Using the actual data class makes the test more realistic.
    """
    return [
        EvaluationResult(metric_name="faithfulness", score=0.9, details="Details for faithfulness"),
        EvaluationResult(metric_name="answer_relevance", score=0.8, details="Details for answer relevance"),
        EvaluationResult(metric_name="context_precision", score=0.7, details="Details for context precision"),
    ]

@pytest.fixture
def reporter_instance(tmp_path: Path) -> Reporter:
    """
    Provides an instance of the Reporter configured to use a temporary output directory.
    
    The `tmp_path` fixture is a special pytest feature that provides a unique
    temporary directory for each test function, ensuring tests don't interfere
    with each other or with the actual file system.
    """
    output_dir = tmp_path / "reports"
    output_dir.mkdir()
    return Reporter(output_dir=str(output_dir))

def test_reporter_initialization(reporter_instance: Reporter, tmp_path: Path):
    """
    Tests that the Reporter is initialized correctly and creates its output directory.
    """
    # Assert
    assert reporter_instance.output_dir.exists()
    assert reporter_instance.output_dir == tmp_path / "reports"

def test_generate_and_save_json_report(reporter_instance: Reporter, sample_evaluation_results_for_report: List[EvaluationResult]):
    """
    Tests the generation and saving of a JSON report.
    """
    # Arrange
    report_path = reporter_instance.output_dir / "report.json"

    # Act
    reporter_instance.generate_report(sample_evaluation_results_for_report, report_format="json")

    # Assert
    assert report_path.exists(), "JSON report file should have been created."
    
    # Check content of the created file
    import json
    with report_path.open('r') as f:
        data = json.load(f)
    
    assert len(data['results']) == 3
    assert data['summary']['total_metrics'] == 3
    assert data['summary']['average_score'] == pytest.approx(0.8) # pytest.approx handles float comparison

def test_generate_and_save_html_report(reporter_instance: Reporter, sample_evaluation_results_for_report: List[EvaluationResult]):
    """
    Tests the generation and saving of an HTML report.
    """
    # Arrange
    report_path = reporter_instance.output_dir / "report.html"

    # Act
    reporter_instance.generate_report(sample_evaluation_results_for_report, report_format="html")

    # Assert
    assert report_path.exists(), "HTML report file should have been created."
    
    # Check that the content seems like valid HTML and contains metric names
    content = report_path.read_text()
    assert "<html>" in content
    assert "faithfulness" in content
    assert "answer_relevance" in content
    assert "Evaluation Report" in content # Check for title

def test_unsupported_report_format(reporter_instance: Reporter, sample_evaluation_results_for_report: List[EvaluationResult]):
    """
    Tests that the reporter handles a request for an unsupported report format gracefully.
    """
    # Act & Assert
    with pytest.raises(ValueError, match="Unsupported report format: xml"):
        reporter_instance.generate_report(sample_evaluation_results_for_report, report_format="xml")