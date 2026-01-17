import json
from datetime import datetime
from typing import List, Dict

LOG_PATH = "data/logs.json"


class SimpleSIEM:
    def __init__(self, log_path: str):
        self.log_path = log_path
        self.events = self._load_logs()

    def _load_logs(self) -> List[Dict]:
        with open(self.log_path, "r") as f:
            return json.load(f)

    def get_all_events(self) -> List[Dict]:
        return self.events

    def filter_by_process(self, process_name: str) -> List[Dict]:
        return [
            e for e in self.events
            if e["process_name"].lower() == process_name.lower()
        ]

    def filter_by_time_range(self, start: str, end: str) -> List[Dict]:
        start_ts = datetime.fromisoformat(start)
        end_ts = datetime.fromisoformat(end)

        results = []
        for e in self.events:
            event_ts = datetime.fromisoformat(e["timestamp"])
            if start_ts <= event_ts <= end_ts:
                results.append(e)
        return results


if __name__ == "__main__":
    siem = SimpleSIEM(LOG_PATH)

    print("\n=== All Events ===")
    for e in siem.get_all_events():
        print(e)

    print("\n=== PowerShell Events ===")
    for e in siem.filter_by_process("powershell.exe"):
        print(e)
