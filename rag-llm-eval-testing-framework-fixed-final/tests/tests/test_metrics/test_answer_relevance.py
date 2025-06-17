import pytest
from typing import Dict, Any
from tests.utils.base_metric_test import BaseMetricTest
from utils.utils.scorer import EvaluationResult

class TestAnswerRelevance(BaseMetricTest):
    """
    Test class for the 'answer_relevance' metric.

    This class inherits from BaseMetricTest to leverage the standardized
    testing framework, including data loading via TestDataHandler and
    common assertion logic.
    """
    # 1. Set the metric name for this test class
    metric_name = "answer_relevance"

    # 2. Implement the metric-specific evaluation logic
    def run_evaluation(self, test_case: Dict[str, Any]) -> EvaluationResult:
        """
        Runs the evaluation for the 'answer_relevance' metric.

        This method extracts the necessary fields from the test case data
        and calls the appropriate scoring function.

        Args:
            test_case: A dictionary containing the data for a single test case.

        Returns:
            The EvaluationResult object from the Scorer.
        """
        # Extract necessary data from the test case
        answer = test_case.get("answer")
        question = test_case.get("question")

        # Ensure the required data is present before scoring
        assert answer is not None, "Test case must contain an 'answer' field."
        assert question is not None, "Test case must contain a 'question' field."

        # Call the specific evaluation method from the shared Scorer instance
        return self.scorer.evaluate_answer_relevance(answer, question)

    # 3. Define the data-driven test function
    @pytest.mark.parametrize("test_case", BaseMetricTest.get_test_cases(metric_name))
    def test_answer_relevance_metric(self, test_case: Dict[str, Any]):
        """
        Data-driven test for the 'answer_relevance' metric.

        This test is automatically parameterized by pytest with every test case
        found in the data files for the 'answer_relevance' metric.

        It calls the standard test logic defined in the BaseMetricTest class.
        """
        # This single call executes the evaluation and all standard assertions
        self.test_metric_logic(test_case)