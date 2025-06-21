import pytest
from typing import Dict, Any
from tests.utils.base_metric_test import BaseMetricTest
from utils.utils.scorer import EvaluationResult

class TestGroundedness(BaseMetricTest):
    """
    Test class for the 'groundedness' metric.
    This tests if the answer is grounded in the provided context.
    """
    metric_name = "groundedness"

    def run_evaluation(self, test_case: Dict[str, Any]) -> EvaluationResult:
        """Runs the evaluation for the 'groundedness' metric."""
        answer = test_case.get("answer")
        context = test_case.get("context")

        assert answer is not None, "Test case must contain an 'answer' field."
        assert context is not None, "Test case must contain a 'context' field."

        return self.scorer.evaluate_groundedness(answer, context)

    @pytest.mark.parametrize("test_case", BaseMetricTest.get_test_cases(metric_name))
    def test_groundedness_metric(self, test_case: Dict[str, Any]):
        """Data-driven test for the 'groundedness' metric."""
        self.test_metric_logic(test_case)
