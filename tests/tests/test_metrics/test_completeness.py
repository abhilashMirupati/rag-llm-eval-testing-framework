import pytest
from typing import Dict, Any
from tests.utils.base_metric_test import BaseMetricTest
from utils.utils.scorer import EvaluationResult

class TestCompleteness(BaseMetricTest):
    """
    Test class for the 'completeness' metric.

    This class tests if the generated answer covers all aspects of the
    given question. It adheres to the standardized testing framework by
    inheriting from BaseMetricTest.
    """
    # 1. Set the metric name for this test class
    metric_name = "completeness"

    # 2. Implement the metric-specific evaluation logic
    def run_evaluation(self, test_case: Dict[str, Any]) -> EvaluationResult:
        """
        Runs the evaluation for the 'completeness' metric.

        This method extracts the question and answer from the test case
        and calls the completeness scoring function.

        Args:
            test_case: A dictionary containing the data for a single test case.

        Returns:
            The EvaluationResult object from the Scorer.
        """
        # Extract necessary data from the test case
        question = test_case.get("question")
        answer = test_case.get("answer")

        # Ensure the required data is present before scoring
        assert question is not None, "Test case must contain a 'question' field."
        assert answer is not None, "Test case must contain an 'answer' field."

        # Call the specific evaluation method from the shared Scorer instance
        return self.scorer.evaluate_completeness(question, answer)

    # 3. Define the data-driven test function
    @pytest.mark.parametrize("test_case", BaseMetricTest.get_test_cases(metric_name))
    def test_completeness_metric(self, test_case: Dict[str, Any]):
        """
        Data-driven test for the 'completeness' metric.

        This test is automatically run for every 'completeness' entry
        in the test data files. It uses the base class to perform assertions.
        """
        # This single call executes the evaluation and all standard assertions
        self.test_metric_logic(test_case)