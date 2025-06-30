import csv
import json
from pathlib import Path


class CSVStorage:
    def __init__(self, output_dir: str):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def save_to_csv(self, obj_name: str, records: list[dict]) -> None:
        if not records:
            return
        cleaned_data = []
        for record in records:
            cleaned_record = {}
            for key, value in record.items():
                if isinstance(value, (dict, list)):
                    cleaned_record[key] = json.dumps(value, ensure_ascii=False)
                elif value is None:
                    cleaned_record[key] = ""
                else:
                    cleaned_record[key] = str(value)
            cleaned_data.append(cleaned_record)

        csv_file = self.output_dir / f"{obj_name.lower()}.csv"
        with open(csv_file, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=cleaned_data[0].keys())
            writer.writeheader()
            writer.writerows(cleaned_data)