/**
 * TypeScript types matching backend models
 */

export type WorkoutType = 'strength' | 'run' | 'recovery';
export type PerceivedEffort = 'easy' | 'moderate' | 'hard';
export type PainSeverity = 'mild' | 'moderate' | 'severe';

export interface Exercise {
  name: string;
  sets?: number;
  reps?: number;
  load?: string;
  notes?: string;
}

export interface RunningData {
  duration_minutes?: number;
  distance_km?: number;
  pace_min_per_km?: number;
  route?: string;
}

export interface PainOrTightness {
  body_areas?: string[];
  description?: string;
  severity?: PainSeverity;
}

export interface MachineContext {
  training_phase?: string;
  overall_fatigue?: string;
  injury_risk?: string;
  problem_areas?: string[];
  movement_quality?: string;
  recommended_focus?: string[];
  load_adjustment?: string;
  confidence_score?: number;
}

export interface AIAnalysis {
  human_insight: string;
  machine_context: MachineContext;
  analyzed_at: string;
}

export interface Metadata {
  created_at: string;
  updated_at: string;
}

export interface WorkoutLog {
  date: string;
  workout_type: WorkoutType;
  exercises?: Exercise[];
  running_data?: RunningData;
  perceived_effort?: PerceivedEffort;
  fatigue_level?: number;
  pain_or_tightness?: PainOrTightness;
  free_text_reflection?: string;
  ai_analysis?: AIAnalysis;
  metadata: Metadata;
}

export interface WorkoutLogCreate {
  date: string;
  workout_type: WorkoutType;
  exercises?: Exercise[];
  running_data?: RunningData;
  perceived_effort?: PerceivedEffort;
  fatigue_level?: number;
  pain_or_tightness?: PainOrTightness;
  free_text_reflection?: string;
}
