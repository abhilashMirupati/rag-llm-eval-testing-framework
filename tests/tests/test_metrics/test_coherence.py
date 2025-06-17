import pytest
from typing import Dict, Any
from tests.utils.base_metric_test import BaseMetricTest
from utils.utils.scorer import EvaluationResult

class TestCoherence(BaseMetricTest):
    """
    Test class for the 'coherence' metric.

    This class tests how logically consistent and well-structured the generated
    answer is. It inherits from BaseMetricTest to ensure it follows the
    standardized, data-driven testing approach.
    """
    # 1. Set the metric name for this test class
    metric_name = "coherence"

    # 2. Implement the metric-specific evaluation logic
    def run_evaluation(self, test_case: Dict[str, Any]) -> EvaluationResult:
        """
        Runs the evaluation for the 'coherence' metric.

        This method extracts the answer from the test case and calls the
        coherence scoring function.

        Args:
            test_case: A dictionary containing the data for a single test case.

        Returns:
            The EvaluationResult object from the Scorer.
        """
        # Extract necessary data from the test case
        answer = test_case.get("answer")

        # Ensure the required data is present before scoring
        assert answer is not None, "Test case must contain an 'answer' field."

        # Call the specific evaluation method from the shared Scorer instance
        return self.scorer.evaluate_coherence(answer)

    # 3. Define the data-driven test function
    @pytest.mark.parametrize("test_case", BaseMetricTest.get_test_cases(metric_name))
    def test_coherence_metric(self, test_case: Dict[str, Any]):
        """
        Data-driven test for the 'coherence' metric.

        This test is automatically run for every 'coherence' entry
        in the test data files. It uses the base class to perform assertions.
        """
        # This single call executes the evaluation and all standard assertions
        self.test_metric_logic(test_case)