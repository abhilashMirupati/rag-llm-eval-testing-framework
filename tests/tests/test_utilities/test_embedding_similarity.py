import pytest
from utils.utils.scorer import Scorer

scorer = Scorer()

@pytest.mark.parametrize("text1, text2, expected_similarity_range", [
    (
        "The sun is shining brightly today.",
        "The sun is shining brightly today.",
        (1.0, 1.0)
    ),
    (
        "The cat sat on the mat.",
        "A feline was resting on the rug.",
        (0.75, 1.0)
    ),
    (
        "France is a country in Western Europe.",
        "What is the capital of France?",
        (0.5, 0.8)
    ),
    (
        "I like to eat pizza.",
        "The international space station orbits the Earth.",
        (0.0, 0.3)
    ),
])
def test_embedding_similarity(text1: str, text2: str, expected_similarity_range: tuple[float, float]):
    """
    Tests the embedding similarity calculation for various sentence pairs.
    """
    embedding1 = scorer.embedding_model.encode([text1])
    embedding2 = scorer.embedding_model.encode([text2])
    similarity_score = scorer.embedding_model.similarity(embedding1, embedding2)[0][0]
    min_expected, max_expected = expected_similarity_range
    assert isinstance(similarity_score, float), "Similarity score should be a float."
    assert min_expected <= similarity_score <= max_expected, \
        f"Similarity score {similarity_score:.2f} for ('{text1}', '{text2}') is outside the expected range of ({min_expected}, {max_expected})."
