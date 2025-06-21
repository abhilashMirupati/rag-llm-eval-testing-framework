import pytest
from typing import Dict, Any
from tests.utils.base_metric_test import BaseMetricTest
from utils.utils.scorer import EvaluationResult

class TestNamedEntities(BaseMetricTest):
    """
    Test class for the 'named_entities' metric.
    
    This single test class verifies the overall score and also asserts on the
    individual sub-metrics (precision and recall) returned in the details.
    """
    metric_name = "named_entities"

    def run_evaluation(self, test_case: Dict[str, Any]) -> EvaluationResult:
        """Runs the evaluation for the 'named_entities' metric."""
        answer = test_case.get("answer")
        context = test_case.get("context")

        assert answer is not None, "Test case must contain an 'answer' field."
        assert context is not None, "Test case must contain a 'context' field."

        return self.scorer.evaluate_named_entities(answer=answer, context=context)

    @pytest.mark.parametrize("test_case", BaseMetricTest.get_test_cases(metric_name))
    def test_named_entities_metric_and_submetrics(self, test_case: Dict[str, Any]):
        """
        Data-driven test for the 'named_entities' metric.
        
        This test performs two levels of checks:
        1. Standard validation of the main score using the base class.
        2. Specific validation of the precision and recall values in the details.
        """
        # --- 1. Standard test for the main score ---
        self.test_metric_logic(test_case)
        
        # --- 2. Specific test for sub-metrics (precision and recall) ---
        result = self.run_evaluation(test_case)
        
        # Check that the details dictionary contains precision and recall
        assert "precision" in result.details, "Details dictionary must contain 'precision'."
        assert "recall" in result.details, "Details dictionary must contain 'recall'."
        
        # If your test data includes expected values, assert against them.
        # Note: You would need to add 'expected_precision' and 'expected_recall'
        # to the corresponding entries in your test_data.json file.
        if "expected_precision" in test_case:
            expected_precision = test_case["expected_precision"]
            assert result.details["precision"] == pytest.approx(expected_precision), \
                f"Precision mismatch: Expected {expected_precision}, Got {result.details['precision']}"

        if "expected_recall" in test_case:
            expected_recall = test_case["expected_recall"]
            assert result.details["recall"] == pytest.approx(expected_recall), \
                f"Recall mismatch: Expected {expected_recall}, Got {result.details['recall']}"
