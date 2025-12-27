# Workout Tracker Backend

FastAPI backend for workout tracking with Claude AI integration.

## Setup

### 1. Create virtual environment

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment

```bash
cp .env.example .env
```

Edit `.env` and add your Anthropic API key:

```
ANTHROPIC_API_KEY=sk-ant-...
CLAUDE_MODEL=claude-sonnet-4-20250514
DATA_DIR=../data
HOST=0.0.0.0
PORT=8000
```

### 4. Run the server

```bash
python main.py
```

Or with uvicorn directly:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

## API Documentation

Once running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

### Workout Logs

- `POST /logs` - Create a new workout log
- `GET /logs` - Get workout logs (with optional date range or recent N days)
- `GET /logs/{date}` - Get a specific log by date
- `PUT /logs/{date}` - Update a workout log
- `DELETE /logs/{date}` - Delete a workout log
- `GET /logs/dates` - List all dates with logs

### AI Analysis

- `POST /analysis/{date}` - Analyze a workout log with Claude AI

### Statistics

- `GET /stats/summary` - Get summary statistics

## Project Structure

```
backend/
├── main.py              # FastAPI application & routes
├── models.py            # Pydantic data models
├── storage.py           # JSON file storage utilities
├── ai_service.py        # Claude AI integration
├── requirements.txt     # Python dependencies
├── .env.example         # Environment variables template
└── README.md           # This file
```

## Development

### Running tests

```bash
pytest
```

### Code quality

```bash
# Format code
black .

# Lint
pylint *.py
```

## Models Overview

### WorkoutLog
Main data model containing:
- Basic info: date, workout_type
- Exercise data: exercises array or running_data
- Subjective feedback: perceived_effort, fatigue_level, pain_or_tightness
- Free-text reflection
- AI analysis (added after analysis)
- Metadata (timestamps)

### AIAnalysis
Contains:
- `human_insight`: Natural language feedback
- `machine_context`: Structured JSON for AI reasoning
- `analyzed_at`: Timestamp

## AI Analysis Process

1. User creates a workout log via POST /logs
2. User requests analysis via POST /analysis/{date}
3. System fetches recent history (default: 7 days)
4. Claude analyzes current workout + history
5. Returns dual output:
   - Human-friendly insight
   - Machine-readable context
6. Analysis is saved to the workout log file

## Notes

- All data stored in JSON files (see ../data/)
- Single-user system (no authentication)
- Claude Sonnet 4 recommended for balance of speed/quality
- Claude Opus 4 available for deeper analysis
