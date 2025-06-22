"""
Test cases for evaluating named entity precision in RAG systems.

Precision measures how many of the named entities identified in the model answer 
are correct, compared to those in the context.
"""

import pytest
from typing import Dict, Any
from tests.utils.base_metric_test import BaseMetricTest
from utils.utils.scorer import EvaluationResult

class TestNamedEntityPrecision(BaseMetricTest):
    """
    Test class for the 'named_entities' metric, focusing on **precision**.

    This test checks the accuracy of named entity extraction in the answer,
    specifically for correct entity types and values present in the context.
    """
    metric_name = "named_entities"

    def run_evaluation(self, test_case: Dict[str, Any]) -> EvaluationResult:
        """Runs the evaluation for named entity precision."""
        answer = test_case.get("answer")
        context = test_case.get("context")

        assert answer is not None, "Test case must contain an 'answer' field."
        assert context is not None, "Test case must contain a 'context' field."

        return self.scorer.evaluate_named_entities(answer=answer, context=context)

    @pytest.mark.parametrize("test_case", BaseMetricTest.get_test_cases(metric_name))
    def test_named_entities_precision(self, test_case: Dict[str, Any]):
        """
        Data-driven test for named entity precision.

        Checks both the overall score and the 'precision' value in the details dict.
        """
        # Standard base assertions
        self.test_metric_logic(test_case)
        # Specific precision sub-metric assertion
        result = self.run_evaluation(test_case)
        assert "precision" in result.details, "Details must include 'precision'."
        # Optionally check an expected_precision if present
        if "expected_precision" in test_case:
            assert result.details["precision"] == pytest.approx(test_case["expected_precision"]), \
                f"Precision mismatch: Expected {test_case['expected_precision']}, Got {result.details['precision']}"
