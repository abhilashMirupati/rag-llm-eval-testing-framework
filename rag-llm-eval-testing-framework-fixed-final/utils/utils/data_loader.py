import pandas as pd
from pathlib import Path
from typing import List, Dict, Any

class DataLoader:
    """Loads datasets for evaluation from various file formats."""

    @staticmethod
    def load_data(file_path: str) -> List[Dict[str, Any]]:
        path = Path(file_path)
        if not path.is_file():
            raise FileNotFoundError(f"Data file not found: {path}")

        extension = path.suffix.lower()
        
        try:
            if extension == '.csv':
                df = pd.read_csv(path)
                return df.where(pd.notna(df), None).to_dict(orient='records')
            elif extension == '.json':
                import json
                with path.open('r', encoding='utf-8') as f:
                    data = json.load(f)
                if isinstance(data, list):
                    return data
                else:
                    raise ValueError("JSON data must be a list of records.")
            else:
                raise ValueError(f"Unsupported file format: {extension}")
        except Exception as e:
            raise ValueError(f"Failed to load or parse data file '{path}': {e}") from e