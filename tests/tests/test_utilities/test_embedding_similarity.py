import pytest
from utils.utils.scorer import Scorer

# A Note on Testing Strategy: Data-Driven vs. Behavior-Driven Tests
#
# You might wonder why this test "hardcodes" data using @pytest.mark.parametrize,
# while other tests (like test_faithfulness.py) load data from external files.
#
# 1. Data-Driven Metric Tests (e.g., test_faithfulness.py):
#    - Purpose: Validate a metric against a large, evolving dataset of real-world examples.
#    - Method: Load data from `tests/data/test_data.json` via the TestDataHandler.
#    - Why: The dataset is too large to list here and changes frequently.
#
# 2. Behavior-Driven Component Tests (This file):
#    - Purpose: Verify a low-level component's core behavior with a few, stable examples.
#    - Method: Use @pytest.mark.parametrize with data directly in the file.
#    - Why: The test cases are a small, clear "specification" of the component's
#      contract (e.g., identical sentences should have a score of 1.0). Keeping
#      this specification with the test makes it self-contained and highly readable.
#
# We use the external data approach for high-level metric validation and the
# internal data approach for low-level component validation.

# Initialize a single Scorer instance to access the embedding model.
# This is efficient as the model is loaded only once.
scorer = Scorer()

@pytest.mark.parametrize("text1, text2, expected_similarity_range", [
    # Case 1: Identical sentences should have a similarity of 1.0
    (
        "The sun is shining brightly today.",
        "The sun is shining brightly today.",
        (1.0, 1.0) # Using a tuple for a range, here it's an exact match
    ),
    # Case 2: Very similar sentences should have high similarity
    (
        "The cat sat on the mat.",
        "A feline was resting on the rug.",
        (0.75, 1.0) # Expect similarity to be high, but not perfect
    ),
    # Case 3: Moderately related sentences
    (
        "France is a country in Western Europe.",
        "What is the capital of France?",
        (0.5, 0.8) # Expect moderate similarity
    ),
    # Case 4: Completely unrelated sentences should have low similarity
    (
        "I like to eat pizza.",
        "The international space station orbits the Earth.",
        (0.0, 0.3) # Expect low similarity
    ),
])
def test_embedding_similarity(text1: str, text2: str, expected_similarity_range: tuple[float, float]):
    """
    Tests the embedding similarity calculation for various sentence pairs.

    This test is parameterized with different cases to check for high,
    moderate, and low similarity, ensuring the embedding model behaves as expected.
    """
    # Arrange
    # Encode the texts using the model from the Scorer
    embedding1 = scorer.embedding_model.encode([text1])
    embedding2 = scorer.embedding_model.encode([text2])
    
    # Act
    # Calculate the cosine similarity
    similarity_score = scorer.embedding_model.similarity(embedding1, embedding2)[0][0]

    # Assert
    # Check that the score falls within the expected range for that case
    min_expected, max_expected = expected_similarity_range
    assert isinstance(similarity_score, float), "Similarity score should be a float."
    assert min_expected <= similarity_score <= max_expected, \
        f"Similarity score {similarity_score:.2f} for ('{text1}', '{text2}') is outside the expected range of ({min_expected}, {max_expected})."