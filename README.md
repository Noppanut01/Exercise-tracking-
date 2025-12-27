# Workout Tracker

A simple, personal workout tracking web app with AI-powered analysis using Claude.

## Overview

This MVP system helps you:
- Track daily workouts (strength, running, recovery)
- Log subjective body feedback (fatigue, soreness, pain)
- Write free-text reflections
- Get AI analysis of your training patterns
- Build structured context for long-term training insights

## Architecture

- **Frontend**: Next.js 15 (TypeScript, App Router, Tailwind CSS)
- **Backend**: FastAPI (Python 3.11+)
- **AI**: Claude (Anthropic API) - Sonnet 4 / Opus 4
- **Storage**: JSON files (one per day, human-readable)

## Project Structure

```
Exercise-tracking-/
├── backend/              # FastAPI backend
│   ├── main.py          # API routes & app
│   ├── models.py        # Pydantic models
│   ├── storage.py       # JSON file handling
│   ├── ai_service.py    # Claude AI integration
│   └── requirements.txt # Python dependencies
├── frontend/            # Next.js frontend
│   ├── app/            # App Router pages
│   ├── components/     # React components
│   ├── lib/            # API client & utilities
│   ├── types/          # TypeScript types
│   └── package.json    # Node dependencies
├── data/               # JSON data storage
│   ├── logs/          # Daily workout logs (YYYY-MM-DD.json)
│   ├── analysis/      # AI analysis results
│   └── schema.json    # JSON Schema definition
└── CONTEXT.md         # Project specification

```

## Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- Anthropic API key (Claude)

### 1. Setup Backend

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY

# Run server
python main.py
```

Backend will run at `http://localhost:8000`

API docs: `http://localhost:8000/docs`

### 2. Setup Frontend

```bash
cd frontend

# Install dependencies
npm install

# Configure environment
cp .env.example .env.local
# Edit .env.local if needed (default points to localhost:8000)

# Run dev server
npm run dev
```

Frontend will run at `http://localhost:3000`

### 3. Start Using

1. Visit `http://localhost:3000`
2. Create your first workout log
3. Add details (exercises, running data, reflections)
4. Request AI analysis
5. Review insights and recommendations

## Features

### Workout Logging
- **Strength workouts**: exercises, sets, reps, load
- **Running workouts**: duration, distance, pace, route
- **Recovery sessions**: light activity, rest days
- **Body feedback**: fatigue level (1-10), pain/tightness, affected areas
- **Free-text reflections**: natural language notes

### AI Analysis (Claude)

For each workout, Claude provides:

**Human Insight**
- Short, encouraging feedback
- Practical recommendations
- Natural language

**Machine Context**
- Training phase assessment
- Overall fatigue level
- Injury risk evaluation
- Problem areas identification
- Movement quality assessment
- Recommended focus areas
- Load adjustment suggestions
- Confidence score

### API Endpoints

#### Logs
- `POST /logs` - Create new log
- `GET /logs` - Get recent logs or date range
- `GET /logs/{date}` - Get specific log
- `PUT /logs/{date}` - Update log
- `DELETE /logs/{date}` - Delete log

#### Analysis
- `POST /analysis/{date}` - Analyze workout with Claude

#### Stats
- `GET /stats/summary` - Summary statistics

## Data Structure

Each daily log (`data/logs/YYYY-MM-DD.json`):

```json
{
  "date": "2025-01-15",
  "workout_type": "strength",
  "exercises": [...],
  "running_data": {...},
  "perceived_effort": "moderate",
  "fatigue_level": 6,
  "pain_or_tightness": {...},
  "free_text_reflection": "...",
  "ai_analysis": {
    "human_insight": "...",
    "machine_context": {...}
  },
  "metadata": {...}
}
```

See `data/schema.json` for complete schema.

## Design Philosophy

- **Simple**: No database, no authentication, single user
- **Readable**: Human-editable JSON files
- **AI-friendly**: Structured data optimized for AI reasoning
- **Extensible**: Clean architecture for future features
- **Safety-focused**: Conservative recommendations, injury prevention

## Non-Goals (for MVP)

- ❌ Authentication / multi-user
- ❌ Database
- ❌ Auto-generated training plans
- ❌ Complex UI
- ❌ Mobile apps

## Future Extensions

- Pattern detection across weeks/months
- Personalized training recommendations
- Integration with wearables
- Advanced visualizations
- Voice logging
- Progressive web app

## Development

### Backend
```bash
cd backend
pytest                    # Run tests
python main.py           # Start server
```

### Frontend
```bash
cd frontend
npm run dev              # Development
npm run build            # Production build
npm run lint             # Linting
```

## Documentation

- [Backend README](./backend/README.md) - FastAPI setup and API details
- [Frontend README](./frontend/README.md) - Next.js setup and structure
- [Data README](./data/README.md) - JSON schema and file structure
- [CONTEXT.md](./CONTEXT.md) - Project specification and decisions

## License

Personal use project.

## Contributing

This is a personal MVP. Fork and adapt as needed.

---

Built with ❤️ for personal fitness tracking and AI-assisted training insights.