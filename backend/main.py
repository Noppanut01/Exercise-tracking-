"""FastAPI backend for workout tracking application."""

import os
from datetime import date, timedelta
from typing import List, Optional
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from models import WorkoutLog, WorkoutLogCreate, AnalysisRequest
from storage import WorkoutStorage
from ai_service import ClaudeAnalyzer

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="Workout Tracker API",
    description="Simple workout tracking with AI analysis",
    version="1.0.0"
)

# CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Next.js default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
storage = WorkoutStorage(data_dir=os.getenv("DATA_DIR", "../data"))
ai_analyzer = ClaudeAnalyzer(
    api_key=os.getenv("ANTHROPIC_API_KEY"),
    model=os.getenv("CLAUDE_MODEL", "claude-sonnet-4-20250514")
)


@app.get("/")
def root():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "Workout Tracker API",
        "version": "1.0.0"
    }


@app.post("/logs", response_model=WorkoutLog, status_code=201)
def create_log(log_data: WorkoutLogCreate):
    """Create a new workout log."""
    # Check if log already exists for this date
    existing_log = storage.get_log(log_data.date)
    if existing_log:
        raise HTTPException(
            status_code=409,
            detail=f"Log already exists for {log_data.date}. Use PUT to update."
        )

    # Create new log
    log = WorkoutLog(**log_data.model_dump())
    storage.save_log(log)

    return log


@app.get("/logs", response_model=List[WorkoutLog])
def get_logs(
    start_date: Optional[date] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[date] = Query(None, description="End date (YYYY-MM-DD)"),
    days: Optional[int] = Query(7, ge=1, le=90, description="Recent days to fetch")
):
    """
    Get workout logs.

    - If start_date and end_date provided: return logs in range
    - Otherwise: return recent N days
    """
    if start_date and end_date:
        if start_date > end_date:
            raise HTTPException(400, "start_date must be before end_date")
        logs = storage.get_logs_range(start_date, end_date)
    else:
        logs = storage.get_recent_logs(days)

    return logs


@app.get("/logs/{log_date}", response_model=WorkoutLog)
def get_log(log_date: date):
    """Get a specific workout log by date."""
    log = storage.get_log(log_date)

    if not log:
        raise HTTPException(404, f"No log found for {log_date}")

    return log


@app.put("/logs/{log_date}", response_model=WorkoutLog)
def update_log(log_date: date, log_data: WorkoutLogCreate):
    """Update an existing workout log."""
    existing_log = storage.get_log(log_date)

    if not existing_log:
        raise HTTPException(404, f"No log found for {log_date}")

    # Update with new data
    updated_log = WorkoutLog(**log_data.model_dump())
    updated_log.metadata = existing_log.metadata  # Preserve original metadata
    storage.save_log(updated_log)

    return updated_log


@app.delete("/logs/{log_date}", status_code=204)
def delete_log(log_date: date):
    """Delete a workout log."""
    deleted = storage.delete_log(log_date)

    if not deleted:
        raise HTTPException(404, f"No log found for {log_date}")

    return None


@app.get("/logs/dates", response_model=List[date])
def list_log_dates():
    """List all dates that have logs."""
    return storage.list_all_dates()


@app.post("/analysis/{log_date}", response_model=WorkoutLog)
def analyze_workout(log_date: date, include_history_days: int = Query(7, ge=1, le=30)):
    """
    Analyze a workout log using Claude AI.

    This will:
    1. Get the specified log
    2. Get recent history for context
    3. Send to Claude for analysis
    4. Save the analysis back to the log
    """
    # Get the target log
    log = storage.get_log(log_date)
    if not log:
        raise HTTPException(404, f"No log found for {log_date}")

    # Get historical context
    end_date = log_date - timedelta(days=1)  # Exclude current day
    start_date = end_date - timedelta(days=include_history_days - 1)
    history_logs = storage.get_logs_range(start_date, end_date)

    # Analyze with Claude
    try:
        analysis = ai_analyzer.analyze_workout(log, history_logs)
        log.ai_analysis = analysis

        # Save updated log
        storage.save_log(log)

        return log

    except Exception as e:
        raise HTTPException(500, f"AI analysis failed: {str(e)}")


@app.get("/stats/summary")
def get_summary_stats():
    """Get summary statistics across all logs."""
    all_dates = storage.list_all_dates()

    if not all_dates:
        return {
            "total_logs": 0,
            "date_range": None,
            "workout_types": {}
        }

    # Get all logs
    logs = storage.get_logs_range(min(all_dates), max(all_dates))

    # Calculate stats
    workout_types = {}
    for log in logs:
        workout_types[log.workout_type] = workout_types.get(log.workout_type, 0) + 1

    return {
        "total_logs": len(logs),
        "date_range": {
            "first": min(all_dates),
            "last": max(all_dates)
        },
        "workout_types": workout_types
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", 8000)),
        reload=True
    )
