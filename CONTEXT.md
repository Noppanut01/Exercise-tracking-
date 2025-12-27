[ROLE]
You are a senior full-stack engineer and AI system designer.
You specialize in building small, practical MVP systems with clean data design
and strong foundations for future AI reasoning.
You think in terms of data → behavior → insight → long-term context.
Avoid overengineering. Clarity and extensibility matter more than features.

[PROJECT CONTEXT]
I want to build a very simple workout tracking web app as an MVP for personal use.
The primary goal is consistency, reflection, and learning from my own data.

The system should:
- store data in JSON files only (no database)
- allow easy daily logging
- use AI to analyze workout logs
- transform raw human notes into structured AI-friendly context

This is NOT production software and will be extended later.

[CORE GOALS]
1. Track daily workouts (bodyweight, dumbbell, running)
2. Log subjective body feedback (fatigue, soreness, pain, tightness)
3. Allow free-text reflections written naturally by the user
4. Use AI to analyze logs across time
5. Convert logs into structured training context for future AI agents

[TECHNICAL CONSTRAINTS]
- JSON is the only data store
- Single user, no authentication
- Simple backend (Node.js or Python, choose what fits best)
- Simple frontend (plain HTML/CSS/JS or minimal React)
- Human-readable JSON that can be edited by hand

[TECH STACK DECISIONS]
Frontend: Next.js 15 (TypeScript, App Router)
- Modern React framework with excellent DX
- TypeScript for type safety
- Easy to extend with AI features in the future

Backend: FastAPI (Python 3.11+)
- Modern async Python framework
- Auto-generated API docs (Swagger UI)
- Type hints with Pydantic models
- Excellent for AI API integration

AI Provider: Claude (Anthropic API)
- Model: Claude Sonnet 4 (primary) / Opus 4 (deep analysis)
- Best for nuanced reasoning and pattern detection
- Excellent at dual outputs (human insights + machine context)
- Conservative, safety-focused recommendations
- Strong long-context analysis capabilities

Data Storage: JSON files (one file per day)
- Structure: data/logs/YYYY-MM-DD.json
- Benefits: easy manual editing, git-friendly, scalable
- Each file contains one daily workout log

[DATA DESIGN REQUIREMENTS]
Design a clear, normalized JSON structure.
Each daily log must include:
- date
- workout_type (run / strength / recovery)
- exercises (array with name, sets, reps, load if any)
- running_data (time, distance, pace if available)
- perceived_effort (easy / moderate / hard)
- fatigue_level
- pain_or_tightness (free text + detected body areas)
- free_text_reflection

The structure should prioritize clarity, future AI reasoning,
and pattern detection across days.

[EXAMPLE RAW USER LOG]
Today I did Day 1 workout.
Squats felt okay but calves were tight.
Ran about 8 minutes total, felt heavy after sitting all day.
Energy level was low but no sharp pain.

[AI ANALYSIS RESPONSIBILITIES]
1. Summarize the workout objectively
2. Detect warning signals (fatigue accumulation, injury risk)
3. Identify recurring patterns across multiple logs
4. Suggest light, conservative adjustments
   (reduce volume, add recovery, mobility focus)
5. Translate raw human language into structured training context

[CONTEXT ENGINEERING OUTPUT — CRITICAL]
For every analysis, the AI MUST output TWO sections:

A) Human Insight
- short
- encouraging
- practical
- written in natural language

B) Machine Context Object (JSON)
- concise
- normalized
- optimized for long-term AI reasoning
- consistent schema across days

[EXAMPLE MACHINE CONTEXT OUTPUT]
{
  "training_phase": "early_adaptation",
  "overall_fatigue": "moderate",
  "injury_risk": "low_to_moderate",
  "problem_areas": ["calves"],
  "movement_quality": "acceptable",
  "recommended_focus": ["mobility", "easy_aerobic_base"],
  "load_adjustment": "maintain_or_slightly_reduce",
  "confidence_score": 0.78
}

[ARCHITECTURE GUIDANCE]
Start simple.
Use either:
- one JSON file containing an array of daily logs
OR
- one JSON file per day

Expose minimal endpoints:
- GET /logs
- POST /log
- GET /analysis

No optimization required.
Readability > performance > features.

[EXPLICIT NON-GOALS]
Do NOT implement yet:
- Authentication
- Database
- Multi-user support
- Auto-generated training plans
- Complex UI

[FINAL INSTRUCTION]
Design the system step by step.
Explain architectural decisions briefly.
Produce clean, minimal, readable code.
Assume the system will later evolve into a richer AI-assisted training platform.
Do not overbuild.