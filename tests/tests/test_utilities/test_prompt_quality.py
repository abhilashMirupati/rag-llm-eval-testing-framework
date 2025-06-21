"""
Test cases for evaluating prompt quality in RAG systems.
"""

import pytest
from utils.scorer import Scorer

@pytest.fixture
def sample_data():
    """Sample data for prompt quality testing."""
    return {
        "prompts": [
            "What are the benefits of exercise?",
            "How does photosynthesis work?",
            "What is quantum computing?"
        ],
        "contexts": [
            ["Exercise improves cardiovascular health and reduces disease risk.", "Physical activity strengthens muscles and bones.", "Regular exercise benefits mental health."],
            ["Plants use sunlight for photosynthesis.", "Water and CO2 are converted to glucose.", "Oxygen is released as a byproduct."],
            ["Quantum computers use qubits instead of bits.", "Qubits can be in multiple states.", "Quantum computing enables parallel processing."]
        ],
        "expected_scores": [0.8, 0.7, 0.9]
    }

def test_prompt_quality_metric(sample_data):
    """Test the prompt quality metric evaluation."""
    scorer = Scorer()
    
    for prompt, context, expected_score in zip(
        sample_data["prompts"],
        sample_data["contexts"],
        sample_data["expected_scores"]
    ):
        result = scorer.evaluate(prompt, context, None, "prompt_quality")
        assert 0 <= result.score <= 1
        assert isinstance(result.details, dict)
        assert "clarity_score" in result.details
        assert "specificity_score" in result.details
        assert "context_alignment_score" in result.details
        assert abs(result.score - expected_score) < 0.2

@pytest.mark.parametrize("prompt,context,expected_score", [
    (
        "What is the capital of France?",
        ["Paris is the capital city of France."],
        0.9
    ),
    (
        "Tell me about stuff.",
        ["Paris is the capital city of France."],
        0.3
    ),
    (
        "What is the capital of France and what are its main attractions?",
        ["Paris is the capital city of France.", "The Eiffel Tower is in Paris.", "The Louvre Museum is in Paris."],
        0.8
    )
])
def test_prompt_quality_edge_cases(prompt, context, expected_score):
    """Test prompt quality metric with edge cases."""
    scorer = Scorer()
    result = scorer.evaluate(prompt, context, None, "prompt_quality")
    assert abs(result.score - expected_score) < 0.1

def test_prompt_quality_batch_evaluation(sample_data):
    """Test batch evaluation of prompt quality metric."""
    scorer = Scorer()
    results = scorer.batch_evaluate(
        sample_data["prompts"],
        sample_data["contexts"],
        [None] * len(sample_data["prompts"])
    )
    
    assert len(results) == len(sample_data["prompts"])
    for result in results:
        assert "prompt_quality" in result["metrics"]
        assert 0 <= result["metrics"]["prompt_quality"] <= 1
        assert "prompt_quality_details" in result
        assert "clarity_score" in result["prompt_quality_details"]
        assert "specificity_score" in result["prompt_quality_details"]

def test_prompt_quality_with_ambiguous_prompts():
    """Test prompt quality with ambiguous prompts."""
    scorer = Scorer()
    prompt = "Tell me about it."
    context = ["The study found that the drug was effective."]
    
    result = scorer.evaluate(prompt, context, None, "prompt_quality")
    assert result.score < 0.5
    assert "ambiguity_score" in result.details
    assert result.details["ambiguity_score"] > 0.5

def test_prompt_quality_with_complex_prompts():
    """Test prompt quality with complex prompts."""
    scorer = Scorer()
    prompt = "What are the implications of quantum computing on cryptography, and how might it affect current encryption methods in the context of blockchain technology?"
    context = ["Quantum computing uses qubits.", "Current encryption methods may be vulnerable."]
    
    result = scorer.evaluate(prompt, context, None, "prompt_quality")
    assert result.score > 0.7
    assert "complexity_score" in result.details
    assert result.details["complexity_score"] > 0.7
