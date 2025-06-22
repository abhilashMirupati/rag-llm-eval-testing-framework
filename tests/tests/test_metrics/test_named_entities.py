"""
Test cases for evaluating named entities in RAG systems.

This test suite covers both precision and recall sub-metrics
for the named_entities metric, as returned in the details dictionary.
"""

import pytest
from typing import Dict, Any
from tests.utils.base_metric_test import BaseMetricTest
from utils.utils.scorer import EvaluationResult

class TestNamedEntities(BaseMetricTest):
    """
    Test class for the 'named_entities' metric.

    Verifies the overall named entity metric score and asserts on 
    both 'precision' and 'recall' sub-metrics as reported in details.
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

        This test checks:
        1. Standard validation of the overall score (base class)
        2. That precision and recall values are present and correct in details.
        """
        # Standard metric assertions
        self.test_metric_logic(test_case)
        # Check sub-metrics in the details
        result = self.run_evaluation(test_case)
        assert "precision" in result.details, "Details must include 'precision'."
        assert "recall" in result.details, "Details must include 'recall'."
        # Optionally check against expected values, if present in test case
        if "expected_precision" in test_case:
            assert result.details["precision"] == pytest.approx(test_case["expected_precision"]), \
                f"Precision mismatch: Expected {test_case['expected_precision']}, Got {result.details['precision']}"
        if "expected_recall" in test_case:
            assert result.details["recall"] == pytest.approx(test_case["expected_recall"]), \
                f"Recall mismatch: Expected {test_case['expected_recall']}, Got {result.details['recall']}"
