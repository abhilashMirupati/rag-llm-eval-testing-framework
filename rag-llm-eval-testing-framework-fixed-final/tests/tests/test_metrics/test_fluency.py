import pytest
from typing import Dict, Any
from tests.utils.base_metric_test import BaseMetricTest
from utils.utils.scorer import EvaluationResult

class TestFluency(BaseMetricTest):
    """
    Test class for the 'fluency' metric.
    This class tests the grammatical fluency of the generated answer.
    """
    metric_name = "fluency"

    def run_evaluation(self, test_case: Dict[str, Any]) -> EvaluationResult:
        """Runs the evaluation for the 'fluency' metric."""
        answer = test_case.get("answer")
        assert answer is not None, "Test case must contain an 'answer' field."
        return self.scorer.evaluate_fluency(answer)

    @pytest.mark.parametrize("test_case", BaseMetricTest.get_test_cases(metric_name))
    def test_fluency_metric(self, test_case: Dict[str, Any]):
        """Data-driven test for the 'fluency' metric."""
        self.test_metric_logic(test_case)