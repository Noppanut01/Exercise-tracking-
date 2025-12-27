"""Pydantic models for workout tracking."""

from datetime import date, datetime
from enum import Enum
from typing import Optional, List
from pydantic import BaseModel, Field


class WorkoutType(str, Enum):
    """Types of workouts."""
    STRENGTH = "strength"
    RUN = "run"
    RECOVERY = "recovery"


class PerceivedEffort(str, Enum):
    """Subjective effort levels."""
    EASY = "easy"
    MODERATE = "moderate"
    HARD = "hard"


class PainSeverity(str, Enum):
    """Pain/tightness severity levels."""
    MILD = "mild"
    MODERATE = "moderate"
    SEVERE = "severe"


class Exercise(BaseModel):
    """Individual exercise within a workout."""
    name: str = Field(..., description="Exercise name")
    sets: Optional[int] = Field(None, ge=0, description="Number of sets")
    reps: Optional[int] = Field(None, ge=0, description="Repetitions per set")
    load: Optional[str] = Field(None, description="Weight/resistance used")
    notes: Optional[str] = Field(None, description="Exercise-specific notes")


class RunningData(BaseModel):
    """Running-specific metrics."""
    duration_minutes: Optional[float] = Field(None, ge=0, description="Total running time")
    distance_km: Optional[float] = Field(None, ge=0, description="Distance in kilometers")
    pace_min_per_km: Optional[float] = Field(None, ge=0, description="Average pace")
    route: Optional[str] = Field(None, description="Running route")


class PainOrTightness(BaseModel):
    """Physical discomfort or restrictions."""
    body_areas: Optional[List[str]] = Field(default_factory=list, description="Affected body parts")
    description: Optional[str] = Field(None, description="Free-text description")
    severity: Optional[PainSeverity] = Field(None, description="Severity level")


class MachineContext(BaseModel):
    """Structured AI context for machine reasoning."""
    training_phase: Optional[str] = Field(None, description="Current training phase")
    overall_fatigue: Optional[str] = Field(None, description="Cumulative fatigue")
    injury_risk: Optional[str] = Field(None, description="Injury risk level")
    problem_areas: Optional[List[str]] = Field(default_factory=list, description="Areas requiring attention")
    movement_quality: Optional[str] = Field(None, description="Movement quality assessment")
    recommended_focus: Optional[List[str]] = Field(default_factory=list, description="Training recommendations")
    load_adjustment: Optional[str] = Field(None, description="Volume/intensity adjustment")
    confidence_score: Optional[float] = Field(None, ge=0, le=1, description="AI confidence (0-1)")


class AIAnalysis(BaseModel):
    """AI-generated analysis results."""
    human_insight: str = Field(..., description="Natural language feedback")
    machine_context: MachineContext = Field(..., description="Structured context")
    analyzed_at: datetime = Field(default_factory=datetime.utcnow, description="Analysis timestamp")


class Metadata(BaseModel):
    """Log metadata."""
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Creation timestamp")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="Update timestamp")


class WorkoutLog(BaseModel):
    """Complete daily workout log."""
    date: date = Field(..., description="Workout date (YYYY-MM-DD)")
    workout_type: WorkoutType = Field(..., description="Type of workout")
    exercises: Optional[List[Exercise]] = Field(default_factory=list, description="Exercises performed")
    running_data: Optional[RunningData] = Field(None, description="Running metrics")
    perceived_effort: Optional[PerceivedEffort] = Field(None, description="Subjective effort")
    fatigue_level: Optional[int] = Field(None, ge=1, le=10, description="Fatigue (1-10)")
    pain_or_tightness: Optional[PainOrTightness] = Field(None, description="Physical discomfort")
    free_text_reflection: Optional[str] = Field(None, description="User's raw thoughts")
    ai_analysis: Optional[AIAnalysis] = Field(None, description="AI analysis results")
    metadata: Metadata = Field(default_factory=Metadata, description="Log metadata")

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            date: lambda v: v.isoformat()
        }


class WorkoutLogCreate(BaseModel):
    """Request model for creating a workout log."""
    date: date
    workout_type: WorkoutType
    exercises: Optional[List[Exercise]] = None
    running_data: Optional[RunningData] = None
    perceived_effort: Optional[PerceivedEffort] = None
    fatigue_level: Optional[int] = Field(None, ge=1, le=10)
    pain_or_tightness: Optional[PainOrTightness] = None
    free_text_reflection: Optional[str] = None


class AnalysisRequest(BaseModel):
    """Request for AI analysis."""
    date: date = Field(..., description="Date to analyze")
    include_history_days: int = Field(7, ge=1, le=30, description="Days of history to include")
