"""JSON file storage utilities."""

import json
from datetime import date, datetime
from pathlib import Path
from typing import Optional, List
from models import WorkoutLog


class WorkoutStorage:
    """Handles reading/writing workout logs to JSON files."""

    def __init__(self, data_dir: str = "../data"):
        """Initialize storage with data directory path."""
        self.data_dir = Path(data_dir)
        self.logs_dir = self.data_dir / "logs"
        self.analysis_dir = self.data_dir / "analysis"

        # Ensure directories exist
        self.logs_dir.mkdir(parents=True, exist_ok=True)
        self.analysis_dir.mkdir(parents=True, exist_ok=True)

    def _get_log_path(self, log_date: date) -> Path:
        """Get file path for a specific date."""
        return self.logs_dir / f"{log_date.isoformat()}.json"

    def save_log(self, log: WorkoutLog) -> None:
        """Save a workout log to a JSON file."""
        log_path = self._get_log_path(log.date)

        # Update metadata
        if log.metadata:
            log.metadata.updated_at = datetime.utcnow()

        # Convert to dict and handle datetime serialization
        log_dict = json.loads(log.model_dump_json())

        # Write to file with pretty formatting
        with open(log_path, 'w', encoding='utf-8') as f:
            json.dump(log_dict, f, indent=2, ensure_ascii=False)

    def get_log(self, log_date: date) -> Optional[WorkoutLog]:
        """Retrieve a workout log for a specific date."""
        log_path = self._get_log_path(log_date)

        if not log_path.exists():
            return None

        with open(log_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        return WorkoutLog(**data)

    def get_logs_range(self, start_date: date, end_date: date) -> List[WorkoutLog]:
        """Get all logs within a date range (inclusive)."""
        logs = []
        current_date = start_date

        while current_date <= end_date:
            log = self.get_log(current_date)
            if log:
                logs.append(log)
            current_date = current_date.replace(day=current_date.day + 1)

        return logs

    def get_recent_logs(self, days: int = 7) -> List[WorkoutLog]:
        """Get the most recent N days of logs."""
        from datetime import timedelta

        end_date = date.today()
        start_date = end_date - timedelta(days=days - 1)

        return self.get_logs_range(start_date, end_date)

    def delete_log(self, log_date: date) -> bool:
        """Delete a workout log for a specific date."""
        log_path = self._get_log_path(log_date)

        if log_path.exists():
            log_path.unlink()
            return True
        return False

    def list_all_dates(self) -> List[date]:
        """List all dates that have logs."""
        dates = []

        for log_file in sorted(self.logs_dir.glob("*.json")):
            # Skip example files
            if "example" in log_file.name:
                continue

            try:
                # Parse date from filename (YYYY-MM-DD.json)
                date_str = log_file.stem
                log_date = date.fromisoformat(date_str)
                dates.append(log_date)
            except ValueError:
                # Skip files that don't match the date format
                continue

        return dates
