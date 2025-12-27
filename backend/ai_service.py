"""Claude AI integration for workout analysis."""

import json
from typing import List
from anthropic import Anthropic
from models import WorkoutLog, AIAnalysis, MachineContext
from datetime import datetime


class ClaudeAnalyzer:
    """Handles AI-powered workout analysis using Claude."""

    def __init__(self, api_key: str, model: str = "claude-sonnet-4-20250514"):
        """Initialize Claude client."""
        self.client = Anthropic(api_key=api_key)
        self.model = model

    def analyze_workout(
        self,
        current_log: WorkoutLog,
        history_logs: List[WorkoutLog] = None
    ) -> AIAnalysis:
        """
        Analyze a workout log with optional historical context.

        Args:
            current_log: The workout log to analyze
            history_logs: Optional list of recent logs for pattern detection

        Returns:
            AIAnalysis object with human insight and machine context
        """
        # Build the analysis prompt
        prompt = self._build_analysis_prompt(current_log, history_logs)

        # Call Claude API
        response = self.client.messages.create(
            model=self.model,
            max_tokens=2000,
            temperature=0.3,  # Lower temperature for more consistent analysis
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        # Parse the response
        return self._parse_analysis_response(response.content[0].text)

    def _build_analysis_prompt(
        self,
        current_log: WorkoutLog,
        history_logs: List[WorkoutLog] = None
    ) -> str:
        """Build the analysis prompt for Claude."""
        prompt_parts = []

        # System context
        prompt_parts.append("""You are an expert fitness coach and movement analyst. Your role is to:
1. Analyze workout data objectively
2. Detect warning signals (fatigue accumulation, injury risk)
3. Identify patterns across multiple training sessions
4. Provide conservative, safety-focused recommendations
5. Generate both human-friendly insights and structured machine context

Your analysis should be:
- Evidence-based and specific
- Conservative (err on the side of safety)
- Encouraging but honest
- Actionable
""")

        # Current workout data
        prompt_parts.append("\n## CURRENT WORKOUT LOG\n")
        prompt_parts.append(f"Date: {current_log.date}")
        prompt_parts.append(f"Type: {current_log.workout_type}")

        if current_log.exercises:
            prompt_parts.append("\nExercises:")
            for ex in current_log.exercises:
                ex_str = f"- {ex.name}"
                if ex.sets:
                    ex_str += f": {ex.sets} sets"
                if ex.reps:
                    ex_str += f" × {ex.reps} reps"
                if ex.load:
                    ex_str += f" ({ex.load})"
                if ex.notes:
                    ex_str += f"\n  Notes: {ex.notes}"
                prompt_parts.append(ex_str)

        if current_log.running_data:
            prompt_parts.append("\nRunning data:")
            rd = current_log.running_data
            if rd.duration_minutes:
                prompt_parts.append(f"- Duration: {rd.duration_minutes} minutes")
            if rd.distance_km:
                prompt_parts.append(f"- Distance: {rd.distance_km} km")
            if rd.pace_min_per_km:
                prompt_parts.append(f"- Pace: {rd.pace_min_per_km} min/km")
            if rd.route:
                prompt_parts.append(f"- Route: {rd.route}")

        if current_log.perceived_effort:
            prompt_parts.append(f"\nPerceived effort: {current_log.perceived_effort}")

        if current_log.fatigue_level:
            prompt_parts.append(f"Fatigue level: {current_log.fatigue_level}/10")

        if current_log.pain_or_tightness:
            pain = current_log.pain_or_tightness
            if pain.body_areas:
                prompt_parts.append(f"\nAffected areas: {', '.join(pain.body_areas)}")
            if pain.description:
                prompt_parts.append(f"Description: {pain.description}")
            if pain.severity:
                prompt_parts.append(f"Severity: {pain.severity}")

        if current_log.free_text_reflection:
            prompt_parts.append(f"\nUser reflection:\n{current_log.free_text_reflection}")

        # Historical context
        if history_logs:
            prompt_parts.append("\n## RECENT WORKOUT HISTORY\n")
            for log in history_logs[-7:]:  # Last 7 days max
                prompt_parts.append(f"\n{log.date} - {log.workout_type}")
                if log.fatigue_level:
                    prompt_parts.append(f"  Fatigue: {log.fatigue_level}/10")
                if log.pain_or_tightness and log.pain_or_tightness.body_areas:
                    prompt_parts.append(f"  Pain/tightness: {', '.join(log.pain_or_tightness.body_areas)}")

        # Output format instructions
        prompt_parts.append("""

## OUTPUT FORMAT

You MUST provide your analysis in exactly this format:

### HUMAN INSIGHT
[2-3 sentences of encouraging, practical feedback written naturally]

### MACHINE CONTEXT
```json
{
  "training_phase": "early_adaptation|maintenance|progressive_overload|deload",
  "overall_fatigue": "low|moderate|high|very_high",
  "injury_risk": "low|low_to_moderate|moderate|moderate_to_high|high",
  "problem_areas": ["area1", "area2"],
  "movement_quality": "excellent|good|acceptable|poor",
  "recommended_focus": ["focus1", "focus2"],
  "load_adjustment": "increase|maintain|maintain_or_slightly_reduce|reduce|rest",
  "confidence_score": 0.75
}
```

Guidelines:
- Be specific about problem areas and recommendations
- Confidence score should reflect data quality and certainty
- Conservative recommendations prioritize long-term health
- Focus on actionable next steps
""")

        return "\n".join(prompt_parts)

    def _parse_analysis_response(self, response_text: str) -> AIAnalysis:
        """Parse Claude's response into structured AIAnalysis object."""
        # Extract human insight (between HUMAN INSIGHT and MACHINE CONTEXT)
        human_insight = ""
        machine_context_json = ""

        lines = response_text.split("\n")
        in_human_section = False
        in_json_section = False
        json_lines = []

        for line in lines:
            if "HUMAN INSIGHT" in line:
                in_human_section = True
                continue
            elif "MACHINE CONTEXT" in line:
                in_human_section = False
                continue
            elif "```json" in line:
                in_json_section = True
                continue
            elif "```" in line and in_json_section:
                in_json_section = False
                continue

            if in_human_section and line.strip():
                human_insight += line.strip() + " "
            elif in_json_section:
                json_lines.append(line)

        # Parse JSON
        machine_context_json = "\n".join(json_lines)
        machine_context_dict = json.loads(machine_context_json)

        # Create objects
        machine_context = MachineContext(**machine_context_dict)

        return AIAnalysis(
            human_insight=human_insight.strip(),
            machine_context=machine_context,
            analyzed_at=datetime.utcnow()
        )
