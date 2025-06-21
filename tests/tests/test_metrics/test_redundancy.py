import pytest
from typing import Dict, Any
from tests.utils.base_metric_test import BaseMetricTest
from utils.utils.scorer import EvaluationResult

class TestRedundancy(BaseMetricTest):
    """
    Test class for the 'redundancy' metric.
    This class tests for repetitive information within the answer.
    """
    metric_name = "redundancy"

    def run_evaluation(self, test_case: Dict[str, Any]) -> EvaluationResult:
        """Runs the evaluation for the 'redundancy' metric."""
        answer = test_case.get("answer")
        assert answer is not None, "Test case must contain an 'answer' field."
        return self.scorer.evaluate_redundancy(answer)

    @pytest.mark.parametrize("test_case", BaseMetricTest.get_test_cases(metric_name))
    def test_redundancy_metric(self, test_case: Dict[str, Any]):
        """Data-driven test for the 'redundancy' metric."""
        self.test_metric_logic(test_case)
