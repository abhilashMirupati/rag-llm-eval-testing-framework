import json
import pandas as pd
from pathlib import Path
from typing import List, Dict, Any, Union

class TestDataLoader:
    """
    A low-level utility class to load and save raw data from/to CSV and JSON files.
    """

    @staticmethod
    def load_csv(file_path: Union[str, Path]) -> List[Dict[str, Any]]:
        path = Path(file_path)
        if not path.is_file(): return []
        try:
            df = pd.read_csv(path)
            return df.where(pd.notna(df), None).to_dict(orient='records')
        except pd.errors.EmptyDataError:
            return []
        except Exception:
            return []

    @staticmethod
    def load_json(file_path: Union[str, Path]) -> Union[Dict, List]:
        path = Path(file_path)
        if not path.is_file(): return {}
        try:
            with path.open('r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, Exception):
            return {}

    @staticmethod
    def save_json(data: Union[Dict, List], file_path: Union[str, Path]):
        path = Path(file_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open('w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)

    @staticmethod
    def save_csv(data: List[Dict[str, Any]], file_path: Union[str, Path]):
        if not data: return
        path = Path(file_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        df = pd.DataFrame(data)
        df.to_csv(path, index=False)