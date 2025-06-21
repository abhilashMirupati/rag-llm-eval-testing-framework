import pytest
from typing import Dict, Any
from tests.utils.base_metric_test import BaseMetricTest
from utils.utils.scorer import EvaluationResult

class TestOverallQuality(BaseMetricTest):
    """
    Test class for the 'overall_quality' metric.
    This class uses a placeholder for subjective or composite quality scoring.
    """
    metric_name = "overall_quality"

    def run_evaluation(self, test_case: Dict[str, Any]) -> EvaluationResult:
        """Runs the evaluation for the 'overall_quality' metric."""
        answer = test_case.get("answer")
        question = test_case.get("question")
        context = test_case.get("context")

        assert answer is not None, "Test case must contain an 'answer' field."
        assert question is not None, "Test case must contain a 'question' field."
        assert context is not None, "Test case must contain a 'context' field."

        return self.scorer.evaluate_overall_quality(answer=answer, question=question, context=context)

    @pytest.mark.parametrize("test_case", BaseMetricTest.get_test_cases(metric_name))
    def test_overall_quality_metric(self, test_case: Dict[str, Any]):
        """Data-driven test for the 'overall_quality' metric."""
        self.test_metric_logic(test_case)
