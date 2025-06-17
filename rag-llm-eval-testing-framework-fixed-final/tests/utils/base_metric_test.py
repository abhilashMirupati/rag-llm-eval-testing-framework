import pytest
from typing import Dict, Any, List
from utils.utils.scorer import Scorer, EvaluationResult
from tests.utils.test_data_handler import TestDataHandler

class BaseMetricTest:
    """
    A base class for all metric tests to standardize test structure and reduce boilerplate.
    """
    metric_name: str = None
    scorer: Scorer = Scorer()
    data_handler: TestDataHandler = TestDataHandler()

    def run_evaluation(self, test_case: Dict[str, Any]) -> EvaluationResult:
        """
        A placeholder for the evaluation logic.
        Subclasses MUST implement this method.
        """
        raise NotImplementedError("Each metric test must implement its own run_evaluation method.")

    def test_metric_logic(self, test_case: Dict[str, Any]):
        """
        The core test logic that will be called by the actual test functions.
        """
        result = self.run_evaluation(test_case)
        expected_min_score = test_case.get("expected_min_score", 0.0)

        assert isinstance(result.score, float), f"Score should be a float, but got {type(result.score)}."
        assert 0 <= result.score <= 1, f"The score {result.score} is outside the valid range of [0, 1]."
        assert result.score >= expected_min_score, f"The score {result.score} is below the expected minimum of {expected_min_score}."
        assert result.details is not None, "The result object should include evaluation details."

    @classmethod
    def get_test_cases(cls) -> List[Dict[str, Any]]:
        """
        A class method to fetch test cases for the metric specified in the subclass.
        """
        if not cls.metric_name:
            raise ValueError("Subclasses of BaseMetricTest must define a 'metric_name' attribute.")
        return cls.data_handler.get_test_cases(cls.metric_name)