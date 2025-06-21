from pathlib import Path
from typing import Dict, List, Any, Optional
from .test_data_loader import TestDataLoader

class TestDataHandler:
    """
    A high-level manager for test data that provides a clean interface for tests.
    """

    def __init__(self, data_dir: str = "tests/data"):
        self.data_dir = Path(data_dir)
        self.json_path = self.data_dir / "test_data.json"
        self.csv_path = self.data_dir / "test_data.csv"
        self._cached_data: Optional[Dict[str, List[Dict[str, Any]]]] = None

    def _load_data(self) -> Dict[str, List[Dict[str, Any]]]:
        """
        Loads test data from JSON or CSV, prioritizing JSON.
        """
        if self._cached_data is not None:
            return self._cached_data

        data = {}
        if self.json_path.exists():
            loaded_json = TestDataLoader.load_json(self.json_path)
            if isinstance(loaded_json, dict):
                data = loaded_json.get("metrics", {})
        elif self.csv_path.exists():
            all_cases = TestDataLoader.load_csv(self.csv_path)
            grouped_data = {}
            for case in all_cases:
                metric = case.get('metric')
                if metric:
                    grouped_data.setdefault(metric, []).append(case)
            data = grouped_data
        
        self._cached_data = data
        return self._cached_data

    def get_test_cases(self, metric_name: str) -> List[Dict[str, Any]]:
        """
        Retrieves all test cases for a given metric.
        """
        all_data = self._load_data()
        return all_data.get(metric_name, [])

    def clear_cache(self) -> None:
        """Clears the in-memory cache of test data."""
        self._cached_data = None
