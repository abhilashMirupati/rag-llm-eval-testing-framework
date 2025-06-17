import pytest
from typing import Dict, Any
from tests.utils.base_metric_test import BaseMetricTest
from utils.utils.scorer import EvaluationResult

class TestConciseness(BaseMetricTest):
    """
    Test class for the 'conciseness' metric.
    Inherits from BaseMetricTest to use the standard testing framework.
    """
    metric_name = "conciseness"

    def run_evaluation(self, test_case: Dict[str, Any]) -> EvaluationResult:
        """Runs the evaluation for the 'conciseness' metric."""
        answer = test_case.get("answer")
        assert answer is not None, "Test case must contain an 'answer' field."
        return self.scorer.evaluate_conciseness(answer)

    @pytest.mark.parametrize("test_case", BaseMetricTest.get_test_cases(metric_name))
    def test_conciseness_metric(self, test_case: Dict[str, Any]):
        """Data-driven test for the 'conciseness' metric."""
        self.test_metric_logic(test_case)