import pytest
from typing import Dict, Any
from tests.utils.base_metric_test import BaseMetricTest
from utils.utils.scorer import EvaluationResult

class TestHallucination(BaseMetricTest):
    """
    Test class for the 'hallucination' metric.
    Inherits from BaseMetricTest to use the standard testing framework.
    """
    metric_name = "hallucination"

    def run_evaluation(self, test_case: Dict[str, Any]) -> EvaluationResult:
        """Runs the evaluation for the 'hallucination' metric."""
        answer = test_case.get("answer")
        context = test_case.get("context")

        assert answer is not None, "Test case must contain an 'answer' field."
        assert context is not None, "Test case must contain a 'context' field."

        return self.scorer.evaluate_hallucination(answer=answer, context=context)

    @pytest.mark.parametrize("test_case", BaseMetricTest.get_test_cases(metric_name))
    def test_hallucination_metric(self, test_case: Dict[str, Any]):
        """Data-driven test for the 'hallucination' metric."""
        self.test_metric_logic(test_case)