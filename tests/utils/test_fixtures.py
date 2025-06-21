import pytest
from utils.utils.scorer import Scorer
from tests.utils.test_data_handler import TestDataHandler

@pytest.fixture(scope="session")
def scorer() -> Scorer:
    """
    A session-scoped fixture that provides a single instance of the Scorer.
    """
    return Scorer()

@pytest.fixture(scope="session")
def data_handler() -> TestDataHandler:
    """
    A session-scoped fixture for the TestDataHandler.
    """
    return TestDataHandler()
