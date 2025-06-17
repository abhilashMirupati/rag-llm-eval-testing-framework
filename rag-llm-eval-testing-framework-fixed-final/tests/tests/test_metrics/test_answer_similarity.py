import pytest
from typing import Dict, Any
from tests.utils.base_metric_test import BaseMetricTest
from utils.utils.scorer import EvaluationResult

class TestAnswerSimilarity(BaseMetricTest):
    """
    Test class for the 'answer_similarity' metric.

    This class follows the standardized testing framework by inheriting from
    BaseMetricTest. It's responsible for testing how semantically similar
    an answer is to a ground truth answer.
    """
    # 1. Set the metric name for this test class
    metric_name = "answer_similarity"

    # 2. Implement the metric-specific evaluation logic
    def run_evaluation(self, test_case: Dict[str, Any]) -> EvaluationResult:
        """
        Runs the evaluation for the 'answer_similarity' metric.

        This method extracts the answer and the ground truth answer from the
        test case data and calls the appropriate scoring function.

        Args:
            test_case: A dictionary containing the data for a single test case.

        Returns:
            The EvaluationResult object from the Scorer.
        """
        # Extract necessary data from the test case
        answer = test_case.get("answer")
        ground_truth_answer = test_case.get("ground_truth_answer")

        # Ensure the required data is present before scoring
        assert answer is not None, "Test case must contain an 'answer' field."
        assert ground_truth_answer is not None, "Test case must contain a 'ground_truth_answer' field."

        # Call the specific evaluation method from the shared Scorer instance
        return self.scorer.evaluate_answer_similarity(answer, ground_truth_answer)

    # 3. Define the data-driven test function
    @pytest.mark.parametrize("test_case", BaseMetricTest.get_test_cases(metric_name))
    def test_answer_similarity_metric(self, test_case: Dict[str, Any]):
        """
        Data-driven test for the 'answer_similarity' metric.

        This test is automatically run for every 'answer_similarity' entry
        in the test data files. It relies on the base class to perform the
        standard assertions.
        """
        # This single call executes the evaluation and all standard assertions
        self.test_metric_logic(test_case)