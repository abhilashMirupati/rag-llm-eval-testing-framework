import pytest
from typing import Dict, Any
from tests.utils.base_metric_test import BaseMetricTest
from utils.utils.scorer import EvaluationResult

class TestContextPrecision(BaseMetricTest):
    """
    Test class for the 'context_precision' metric.
    Inherits from BaseMetricTest to use the standard testing framework.
    """
    metric_name = "context_precision"

    def run_evaluation(self, test_case: Dict[str, Any]) -> EvaluationResult:
        """Runs the evaluation for the 'context_precision' metric."""
        question = test_case.get("question")
        answer = test_case.get("answer")
        context = test_case.get("context")

        assert question is not None, "Test case must contain a 'question' field."
        assert answer is not None, "Test case must contain an 'answer' field."
        assert context is not None, "Test case must contain a 'context' field."
        
        return self.scorer.evaluate_context_precision(question=question, answer=answer, context=context)

    @pytest.mark.parametrize("test_case", BaseMetricTest.get_test_cases(metric_name))
    def test_context_precision_metric(self, test_case: Dict[str, Any]):
        """Data-driven test for the 'context_precision' metric."""
        self.test_metric_logic(test_case)