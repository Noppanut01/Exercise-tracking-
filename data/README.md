# Data Directory Structure

This directory contains all workout data in JSON format.

## Directory Layout

```
data/
├── schema.json              # JSON Schema definition for workout logs
├── logs/                    # Daily workout logs (one file per day)
│   ├── 2025-01-15.json
│   ├── 2025-01-16.json
│   └── ...
└── analysis/                # AI analysis results (weekly/monthly summaries)
    ├── weekly-2025-W03.json
    └── ...
```

## File Naming Convention

- **Daily logs**: `YYYY-MM-DD.json` (e.g., `2025-01-15.json`)
- **Weekly analysis**: `weekly-YYYY-WNN.json` (e.g., `weekly-2025-W03.json`)
- **Monthly analysis**: `monthly-YYYY-MM.json` (e.g., `monthly-2025-01.json`)

## Daily Log Structure

Each daily log file follows the schema defined in `schema.json`. See `logs/2025-01-15-example.json` for a complete example.

### Required Fields
- `date`: ISO 8601 date (YYYY-MM-DD)
- `workout_type`: "strength" | "run" | "recovery"

### Optional Fields
- `exercises`: Array of exercise objects (for strength workouts)
- `running_data`: Running metrics (for run workouts)
- `perceived_effort`: "easy" | "moderate" | "hard"
- `fatigue_level`: 1-10 scale
- `pain_or_tightness`: Body feedback
- `free_text_reflection`: Raw user thoughts
- `ai_analysis`: Added after AI processes the log
- `metadata`: Timestamps

## Manual Editing

All JSON files are human-readable and can be edited manually. Use proper JSON formatting to avoid parsing errors.

## AI Analysis

The `ai_analysis` field is automatically added by the system when logs are analyzed. It contains:
- `human_insight`: Natural language feedback
- `machine_context`: Structured data for AI reasoning
- `analyzed_at`: Timestamp

## Backup

It's recommended to version control this directory with git. Each file represents a single day, making it easy to track changes over time.
