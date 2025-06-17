import pytest
from typing import Dict, Any
from tests.utils.base_metric_test import BaseMetricTest
from utils.utils.scorer import EvaluationResult

class TestFaithfulness(BaseMetricTest):
    """
    Test class for the 'faithfulness' metric.
    Inherits from BaseMetricTest to use the standard testing framework.
    """
    metric_name = "faithfulness"

    def run_evaluation(self, test_case: Dict[str, Any]) -> EvaluationResult:
        """Runs the evaluation for the 'faithfulness' metric."""
        answer = test_case.get("answer")
        context = test_case.get("context")

        assert answer is not None, "Test case must contain an 'answer' field."
        assert context is not None, "Test case must contain a 'context' field."

        return self.scorer.evaluate_faithfulness(answer=answer, context=context)

    @pytest.mark.parametrize("test_case", BaseMetricTest.get_test_cases(metric_name))
    def test_faithfulness_metric(self, test_case: Dict[str, Any]):
        """Data-driven test for the 'faithfulness' metric."""
        self.test_metric_logic(test_case)