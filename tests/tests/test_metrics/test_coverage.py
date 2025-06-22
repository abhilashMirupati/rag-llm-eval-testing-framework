"""
Test cases for evaluating coverage in RAG systems.
Coverage measures how well the response covers the relevant information from the context.
"""

import pytest
from utils.scorer import Scorer
from utils.utils.metrics_manager import MetricsManager

@pytest.fixture
def sample_data():
    """Sample data for coverage testing."""
    return {
        "questions": [
            "What are the benefits of exercise?",
            "How does photosynthesis work?",
            "What is quantum computing?"
        ],
        "answers": [
            "Regular exercise has numerous benefits including improved cardiovascular health, increased muscle strength, and better mental health. It can help reduce the risk of chronic diseases and improve overall quality of life.",
            "Photosynthesis is the process by which plants convert light energy into chemical energy. They use sunlight, water, and carbon dioxide to produce glucose and oxygen.",
            "Quantum computing uses quantum bits or qubits to perform calculations. Unlike classical computers that use binary bits, qubits can exist in multiple states simultaneously, enabling parallel processing."
        ],
        "contexts": [
            ["Exercise improves cardiovascular health and reduces disease risk.", "Physical activity strengthens muscles and bones.", "Regular exercise benefits mental health."],
            ["Plants use sunlight for photosynthesis.", "Water and CO2 are converted to glucose.", "Oxygen is released as a byproduct."],
            ["Quantum computers use qubits instead of bits.", "Qubits can be in multiple states.", "Quantum computing enables parallel processing."]
        ]
    }

@pytest.mark.parametrize("answer,context,expected_score", [
    (
        "The capital of France is Paris.",
        ["Paris is the capital city of France."],
        1.0
    ),
    (
        "The capital of France is Paris.",
        ["Paris is the capital city of France.", "France is in Europe.", "Paris has the Eiffel Tower."],
        0.33
    ),
    (
        "The capital of France is Paris, which is known for the Eiffel Tower and the Louvre Museum.",
        ["Paris is the capital city of France.", "The Eiffel Tower is in Paris.", "The Louvre Museum is in Paris."],
        1.0
    )
])
def test_coverage_edge_cases(answer, context, expected_score):
    """Test coverage metric with edge cases."""
    scorer = Scorer()
    result = scorer.evaluate(answer, context, "What is the capital of France?", "coverage")
    assert abs(result.score - expected_score) < 0.1

def test_coverage_metric(sample_data):
    """Test the coverage metric evaluation."""
    scorer = Scorer()
    for q, a, c in zip(sample_data["questions"], sample_data["answers"], sample_data["contexts"]):
        result = scorer.evaluate(a, c, q, "coverage")
        assert 0 <= result.score <= 1
        assert isinstance(result.details, dict)
        assert "covered_points" in result.details
        assert "missed_points" in result.details
        assert "coverage_ratio" in result.details

def test_coverage_batch_evaluation(sample_data):
    """Test batch evaluation of coverage metric."""
    scorer = Scorer()
    results = scorer.batch_evaluate(
        sample_data["answers"],
        sample_data["contexts"],
        sample_data["questions"]
    )
    assert len(results) == len(sample_data["questions"])
    for result in results:
        assert "coverage" in result["metrics"]
        assert 0 <= result["metrics"]["coverage"] <= 1
        assert "coverage_details" in result
        assert "covered_points" in result["coverage_details"]
        assert "missed_points" in result["coverage_details"]

def test_coverage_with_partial_information():
    """Test coverage with partial information coverage."""
    scorer = Scorer()
    answer = "The company reported $1M in revenue."
    context = ["The company reported $1M in revenue.", "The company has 50 employees.", "The company was founded in 2020."]
    result = scorer.evaluate(answer, context, "What are the company's key metrics?", "coverage")
    assert 0 < result.score < 1
    assert "partial_coverage" in result.details
    assert len(result.details["partial_coverage"]) > 0

def test_coverage_with_redundant_information():
    """Test coverage with redundant information."""
    scorer = Scorer()
    answer = "The study found that the drug was effective. The study found that the drug was effective."
    context = ["The study found that the drug was effective."]
    result = scorer.evaluate(answer, context, "What were the study findings?", "coverage")
    assert result.score == 1.0
    assert "redundant_information" in result.details
    assert len(result.details["redundant_information"]) > 0

@pytest.mark.parametrize("answer,context,ground_truth", [
    (
        "Regular exercise has numerous benefits including improved cardiovascular health, increased muscle strength, and better mental health. It can help reduce the risk of chronic diseases and improve overall quality of life.",
        "Exercise has numerous health benefits including improved heart health, increased muscle mass, and better mental health.",
        "Exercise provides various health benefits such as improved cardiovascular health, increased muscle strength, and enhanced mental well-being."
    )
])
def test_coverage_manager_calculation(answer, context, ground_truth):
    metrics_manager = MetricsManager()
    score, details = metrics_manager.calculate_coverage(answer=answer, context=context)
    assert isinstance(score, float)
    assert 0.0 <= score <= 1.0
    assert isinstance(details, dict)

def test_coverage_with_empty_inputs():
    metrics_manager = MetricsManager()
    score, details = metrics_manager.calculate_coverage("", "")
    assert score == 0.0
    assert isinstance(details, dict)

def test_coverage_with_partial_content():
    metrics_manager = MetricsManager()
    score, details = metrics_manager.calculate_coverage(
        "Exercise is good for health.",
        "Exercise has numerous health benefits including improved heart health, increased muscle mass, and better mental health."
    )
    assert score < 0.7
    assert isinstance(details, dict)

def test_coverage_with_extra_content():
    metrics_manager = MetricsManager()
    answer = "Regular exercise has numerous benefits including improved cardiovascular health, increased muscle strength, and better mental health. It can help reduce the risk of chronic diseases and improve overall quality of life. Additional unrelated information about cooking."
    context = "Exercise has numerous health benefits including improved heart health, increased muscle mass, and better mental health."
    score, details = metrics_manager.calculate_coverage(answer, context)
    assert score < 1.0
    assert isinstance(details, dict)
