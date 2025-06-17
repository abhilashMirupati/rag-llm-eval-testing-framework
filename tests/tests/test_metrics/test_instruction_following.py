import pytest
from typing import Dict, Any
from tests.utils.base_metric_test import BaseMetricTest
from utils.utils.scorer import EvaluationResult

class TestInstructionFollowing(BaseMetricTest):
    """
    Test class for the 'instruction_following' metric.
    This class tests if the answer adheres to a specific instruction.
    """
    metric_name = "instruction_following"

    def run_evaluation(self, test_case: Dict[str, Any]) -> EvaluationResult:
        """Runs the evaluation for the 'instruction_following' metric."""
        answer = test_case.get("answer")
        # Note: This metric requires an "instruction" field in your test data.
        instruction = test_case.get("instruction")

        assert answer is not None, "Test case must contain an 'answer' field."
        assert instruction is not None, "Test case for this metric must contain an 'instruction' field."

        return self.scorer.evaluate_instruction_following(answer=answer, instruction=instruction)

    @pytest.mark.parametrize("test_case", BaseMetricTest.get_test_cases(metric_name))
    def test_instruction_following_metric(self, test_case: Dict[str, Any]):
        """Data-driven test for the 'instruction_following' metric."""
        self.test_metric_logic(test_case)