"""
Test cases for evaluating named entity recall in RAG systems.
Named entity recall measures the completeness of named entities in the response compared to the context.
"""

import pytest
from utils.scorer import Scorer

@pytest.fixture
def sample_data():
    """Sample data for named entity recall testing."""
    return {
        "questions": [
            "Who is the CEO of Apple?",
            "What is the capital of France?",
            "When was the Eiffel Tower built?"
        ],
        "answers": [
            "Tim Cook is the CEO of Apple Inc.",
            "Paris is the capital of France.",
            "The Eiffel Tower was built in 1889."
        ],
        "contexts": [
            ["Tim Cook has been the CEO of Apple since 2011.", "Apple Inc. is headquartered in Cupertino."],
            ["Paris has been the capital of France since 987.", "The city is known for the Eiffel Tower."],
            ["The Eiffel Tower was completed in 1889.", "It was designed by Gustave Eiffel."]
        ],
        "expected_scores": [1.0, 1.0, 1.0]
    }

def test_named_entity_recall_metric(sample_data):
    """Test the named entity recall metric evaluation."""
    scorer = Scorer()
    
    for q, a, c, expected_score in zip(sample_data["questions"], sample_data["answers"], sample_data["contexts"], sample_data["expected_scores"]):
        result = scorer.evaluate(a, c, q, "named_entity_recall")
        assert 0 <= result.score <= 1
        assert isinstance(result.details, dict)
        assert "retrieved_entities" in result.details
        assert "missing_entities" in result.details
        assert "entity_types" in result.details

@pytest.mark.parametrize("answer,context,expected_score", [
    (
        "The Eiffel Tower was built in 1889.",
        ["The Eiffel Tower was completed in 1889.", "It was designed by Gustave Eiffel."],
        0.5
    ),
    (
        "The Eiffel Tower was built in 1889 by Gustave Eiffel.",
        ["The Eiffel Tower was completed in 1889.", "It was designed by Gustave Eiffel."],
        1.0
    ),
    (
        "The Tower was built in 1889.",
        ["The Eiffel Tower was completed in 1889.", "It was designed by Gustave Eiffel."],
        0.0
    )
])
def test_named_entity_recall_edge_cases(answer, context, expected_score):
    """Test named entity recall metric with edge cases."""
    scorer = Scorer()
    result = scorer.evaluate(answer, context, "When was the Eiffel Tower built?", "named_entity_recall")
    assert abs(result.score - expected_score) < 0.1

def test_named_entity_recall_batch_evaluation(sample_data):
    """Test batch evaluation of named entity recall metric."""
    scorer = Scorer()
    results = scorer.batch_evaluate(
        sample_data["answers"],
        sample_data["contexts"],
        sample_data["questions"]
    )
    
    assert len(results) == len(sample_data["questions"])
    for result in results:
        assert "named_entity_recall" in result["metrics"]
        assert 0 <= result["metrics"]["named_entity_recall"] <= 1
        assert "named_entity_recall_details" in result
        assert "retrieved_entities" in result["named_entity_recall_details"]
        assert "entity_types" in result["named_entity_recall_details"]

def test_named_entity_recall_with_multiple_entities():
    """Test named entity recall with multiple entities."""
    scorer = Scorer()
    answer = "Apple was founded by Steve Jobs and Steve Wozniak in 1976."
    context = ["Apple Inc. was founded by Steve Jobs and Steve Wozniak in 1976.", "The company is headquartered in Cupertino, California."]
    
    result = scorer.evaluate(answer, context, "Who founded Apple?", "named_entity_recall")
    assert result.score > 0.8
    assert len(result.details["retrieved_entities"]) >= 3
    assert "PERSON" in result.details["entity_types"]
    assert "ORG" in result.details["entity_types"]
    assert "DATE" in result.details["entity_types"]

def test_named_entity_recall_with_missing_entities():
    """Test named entity recall with missing entities."""
    scorer = Scorer()
    answer = "The company was founded in 1976."
    context = ["Apple Inc. was founded by Steve Jobs and Steve Wozniak in 1976.", "The company is headquartered in Cupertino, California."]
    
    result = scorer.evaluate(answer, context, "Who founded the company?", "named_entity_recall")
    assert result.score < 0.5
    assert "missing_entities" in result.details
    assert len(result.details["missing_entities"]) > 0

def test_named_entity_recall_with_implicit_entities():
    """Test named entity recall with implicit entities."""
    scorer = Scorer()
    answer = "The tech giant was founded in California."
    context = ["Apple Inc. was founded in Cupertino, California."]
    
    result = scorer.evaluate(answer, context, "Where was the company founded?", "named_entity_recall")
    assert 0.5 <= result.score <= 0.7
    assert "implicit_entities" in result.details
    assert len(result.details["implicit_entities"]) > 0 