import pytest
from typing import Dict, Any
from tests.utils.base_metric_test import BaseMetricTest
from utils.utils.scorer import EvaluationResult

class TestContextRelevance(BaseMetricTest):
    """
    Test class for the 'context_relevance' metric.

    This class tests how relevant the retrieved context is to the user's
    question. It adheres to the standardized testing framework by
    inheriting from BaseMetricTest.
    """
    # 1. Set the metric name for this test class
    metric_name = "context_relevance"

    # 2. Implement the metric-specific evaluation logic
    def run_evaluation(self, test_case: Dict[str, Any]) -> EvaluationResult:
        """
        Runs the evaluation for the 'context_relevance' metric.

        This method extracts the question and context from the test case
        and calls the context_relevance scoring function.

        Args:
            test_case: A dictionary containing the data for a single test case.

        Returns:
            The EvaluationResult object from the Scorer.
        """
        # Extract necessary data from the test case
        question = test_case.get("question")
        context = test_case.get("context")

        # Ensure the required data is present before scoring
        assert question is not None, "Test case must contain a 'question' field."
        assert context is not None, "Test case must contain a 'context' field."

        # Call the newly implemented evaluation method from the shared Scorer instance
        return self.scorer.evaluate_context_relevance(question, context)

    # 3. Define the data-driven test function
    @pytest.mark.parametrize("test_case", BaseMetricTest.get_test_cases(metric_name))
    def test_context_relevance_metric(self, test_case: Dict[str, Any]):
        """
        Data-driven test for the 'context_relevance' metric.

        This test is automatically run for every 'context_relevance' entry
        in the test data files. It uses the base class to perform assertions.
        """
        # This single call executes the evaluation and all standard assertions
        self.test_metric_logic(test_case)
