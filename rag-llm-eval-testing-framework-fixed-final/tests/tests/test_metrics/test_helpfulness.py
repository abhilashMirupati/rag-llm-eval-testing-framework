import pytest
from typing import Dict, Any
from tests.utils.base_metric_test import BaseMetricTest
from utils.utils.scorer import EvaluationResult

class TestHelpfulness(BaseMetricTest):
    """
    Test class for the 'helpfulness' metric.
    Inherits from BaseMetricTest to use the standard testing framework.
    """
    metric_name = "helpfulness"

    def run_evaluation(self, test_case: Dict[str, Any]) -> EvaluationResult:
        """Runs the evaluation for the 'helpfulness' metric."""
        question = test_case.get("question")
        answer = test_case.get("answer")

        assert question is not None, "Test case must contain a 'question' field."
        assert answer is not None, "Test case must contain an 'answer' field."

        return self.scorer.evaluate_helpfulness(question=question, answer=answer)

    @pytest.mark.parametrize("test_case", BaseMetricTest.get_test_cases(metric_name))
    def test_helpfulness_metric(self, test_case: Dict[str, Any]):
        """Data-driven test for the 'helpfulness' metric."""
        self.test_metric_logic(test_case)