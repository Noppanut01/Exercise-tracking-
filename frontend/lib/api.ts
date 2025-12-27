/**
 * API client for backend communication
 */

import { WorkoutLog, WorkoutLogCreate } from '@/types';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

class APIClient {
  private baseUrl: string;

  constructor(baseUrl: string) {
    this.baseUrl = baseUrl;
  }

  private async request<T>(
    endpoint: string,
    options?: RequestInit
  ): Promise<T> {
    const url = `${this.baseUrl}${endpoint}`;
    const response = await fetch(url, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...options?.headers,
      },
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: 'Unknown error' }));
      throw new Error(error.detail || `HTTP ${response.status}`);
    }

    return response.json();
  }

  // Health check
  async healthCheck() {
    return this.request<{ status: string }>('/');
  }

  // Get recent logs
  async getLogs(days: number = 7): Promise<WorkoutLog[]> {
    return this.request<WorkoutLog[]>(`/logs?days=${days}`);
  }

  // Get logs in date range
  async getLogsRange(startDate: string, endDate: string): Promise<WorkoutLog[]> {
    return this.request<WorkoutLog[]>(`/logs?start_date=${startDate}&end_date=${endDate}`);
  }

  // Get single log by date
  async getLog(date: string): Promise<WorkoutLog> {
    return this.request<WorkoutLog>(`/logs/${date}`);
  }

  // Create new log
  async createLog(log: WorkoutLogCreate): Promise<WorkoutLog> {
    return this.request<WorkoutLog>('/logs', {
      method: 'POST',
      body: JSON.stringify(log),
    });
  }

  // Update existing log
  async updateLog(date: string, log: WorkoutLogCreate): Promise<WorkoutLog> {
    return this.request<WorkoutLog>(`/logs/${date}`, {
      method: 'PUT',
      body: JSON.stringify(log),
    });
  }

  // Delete log
  async deleteLog(date: string): Promise<void> {
    await this.request<void>(`/logs/${date}`, {
      method: 'DELETE',
    });
  }

  // Request AI analysis
  async analyzeLog(date: string, historyDays: number = 7): Promise<WorkoutLog> {
    return this.request<WorkoutLog>(`/analysis/${date}?include_history_days=${historyDays}`);
  }

  // Get summary stats
  async getSummaryStats() {
    return this.request<{
      total_logs: number;
      date_range: { first: string; last: string } | null;
      workout_types: Record<string, number>;
    }>('/stats/summary');
  }

  // List all log dates
  async getLogDates(): Promise<string[]> {
    return this.request<string[]>('/logs/dates');
  }
}

export const api = new APIClient(API_URL);
