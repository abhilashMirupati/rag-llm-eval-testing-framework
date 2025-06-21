import pytest
from typing import Dict, Any
from tests.utils.base_metric_test import BaseMetricTest
from utils.utils.scorer import EvaluationResult

class TestQaMatch(BaseMetricTest):
    """
    Test class for the 'qa_match' metric using embedding similarity.
    """
    metric_name = "qa_match"

    def run_evaluation(self, test_case: Dict[str, Any]) -> EvaluationResult:
        """Runs the evaluation for the 'qa_match' metric."""
        question = test_case.get("question")
        answer = test_case.get("answer")
        ground_truth = test_case.get("ground_truth")

        assert question is not None, "Test case must contain a 'question' field."
        assert answer is not None, "Test case must contain an 'answer' field."
        assert ground_truth is not None, "Test case must contain a 'ground_truth' field."

        return self.scorer.evaluate_qa_match(answer=answer, question=question, ground_truth=ground_truth)

    @pytest.mark.parametrize("test_case", BaseMetricTest.get_test_cases(metric_name))
    def test_qa_match_metric(self, test_case: Dict[str, Any]):
        """Data-driven test for the 'qa_match' metric."""
        self.test_metric_logic(test_case)
