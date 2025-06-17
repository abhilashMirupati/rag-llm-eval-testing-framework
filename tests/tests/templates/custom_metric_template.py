import pytest
from typing import Dict, Any
from tests.utils.base_metric_test import BaseMetricTest
from utils.utils.scorer import EvaluationResult

# --- How to Create a Custom Metric Test ---
#
# 1. Copy this file and rename it to 'test_<your_metric_name>.py'.
#
# 2. Change the class name from 'TestCustomMetricTemplate' to 'Test<YourMetricName>'.
#
# 3. Update the 'metric_name' attribute to match the name of your metric.
#    This name MUST correspond to the 'metric' key in your test data file.
#
# 4. Implement your custom scoring logic in the 'run_evaluation' method.
#    - Extract the required input fields from the 'test_case' dictionary.
#    - Perform your calculations.
#    - Return an 'EvaluationResult' object containing the score and details.
#
# 5. Add test data for your new metric in 'tests/data/test_data.json' or
#    'tests/data/test_data.csv'.
#
# ---------------------------------------------------------------------------

class TestCustomMetricTemplate(BaseMetricTest):
    """
    A template for creating new, custom metric tests.
    
    To create a new test, copy this file and follow the instructions above.
    """
    # TODO: Step 1 - Set a unique name for your custom metric.
    # This name must match the 'metric' key in your test data file.
    metric_name = "custom_metric_name"

    def run_evaluation(self, test_case: Dict[str, Any]) -> EvaluationResult:
        """
        TODO: Step 2 - Implement your custom evaluation logic here.

        This method defines how your custom metric is calculated.

        Args:
            test_case: A dictionary loaded from your test data file, containing
                       all the necessary inputs for this metric.

        Returns:
            An EvaluationResult object with the calculated score and any
            relevant details for context.
        """
        # a) Extract the necessary inputs from the test case dictionary.
        #    Example:
        # custom_input = test_case.get("your_custom_input_field")
        # assert custom_input is not None, "Test case must contain 'your_custom_input_field'."

        # b) Implement your custom scoring logic here.
        #    This could involve making API calls, running calculations, etc.
        #    For this template, we'll use a placeholder score.
        score = 1.0  # Replace with your actual score calculation.
        details = "This is a placeholder detail string for the custom metric."

        # c) Return the result as an EvaluationResult object.
        #    The 'score' should be a float between 0.0 and 1.0.
        #    The 'details' can be any string providing context or explanation.
        return EvaluationResult(score=score, details=details)

    # Step 3: The test function itself.
    # This part usually doesn't need to be changed.
    @pytest.mark.parametrize("test_case", BaseMetricTest.get_test_cases(metric_name))
    def test_custom_metric(self, test_case: Dict[str, Any]):
        """
        Data-driven test for your custom metric.
        
        This test will automatically run for every entry corresponding to
        your 'metric_name' in the test data files. It uses the standard
        assertion logic from the base class.
        """
        self.test_metric_logic(test_case)