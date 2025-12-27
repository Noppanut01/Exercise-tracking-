'use client';

import { useEffect, useState } from 'react';
import { api } from '@/lib/api';
import { WorkoutLog } from '@/types';

export default function Home() {
  const [recentLogs, setRecentLogs] = useState<WorkoutLog[]>([]);
  const [stats, setStats] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      setLoading(true);
      const [logs, statsData] = await Promise.all([
        api.getLogs(7),
        api.getSummaryStats(),
      ]);
      setRecentLogs(logs);
      setStats(statsData);
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load data');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="text-gray-500">Loading...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-50 border border-red-200 rounded-lg p-4">
        <h3 className="text-red-800 font-medium">Error</h3>
        <p className="text-red-600 text-sm mt-1">{error}</p>
        <p className="text-red-600 text-sm mt-2">
          Make sure the backend is running at {process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}
        </p>
      </div>
    );
  }

  return (
    <div>
      <div className="mb-8">
        <h2 className="text-2xl font-bold text-gray-900 mb-4">Dashboard</h2>

        {/* Stats */}
        {stats && (
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
            <div className="bg-white rounded-lg shadow p-6">
              <h3 className="text-sm font-medium text-gray-500">Total Workouts</h3>
              <p className="text-3xl font-bold text-gray-900 mt-2">{stats.total_logs}</p>
            </div>
            <div className="bg-white rounded-lg shadow p-6">
              <h3 className="text-sm font-medium text-gray-500">Date Range</h3>
              <p className="text-lg font-medium text-gray-900 mt-2">
                {stats.date_range ? (
                  <>
                    {stats.date_range.first} to {stats.date_range.last}
                  </>
                ) : (
                  'No logs yet'
                )}
              </p>
            </div>
            <div className="bg-white rounded-lg shadow p-6">
              <h3 className="text-sm font-medium text-gray-500">Workout Types</h3>
              <div className="mt-2 space-y-1">
                {Object.entries(stats.workout_types || {}).map(([type, count]) => (
                  <div key={type} className="flex justify-between text-sm">
                    <span className="capitalize text-gray-700">{type}</span>
                    <span className="font-medium text-gray-900">{count as number}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {/* Recent Logs */}
        <h3 className="text-xl font-semibold text-gray-900 mb-4">Recent Workouts</h3>
        {recentLogs.length === 0 ? (
          <div className="bg-white rounded-lg shadow p-8 text-center">
            <p className="text-gray-500">No workout logs yet.</p>
            <a
              href="/log"
              className="mt-4 inline-block bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700"
            >
              Create your first log
            </a>
          </div>
        ) : (
          <div className="space-y-4">
            {recentLogs.map((log) => (
              <div key={log.date} className="bg-white rounded-lg shadow p-6">
                <div className="flex justify-between items-start">
                  <div>
                    <h4 className="text-lg font-medium text-gray-900">{log.date}</h4>
                    <span className="inline-block mt-1 px-2 py-1 text-xs font-medium rounded-full bg-blue-100 text-blue-800 capitalize">
                      {log.workout_type}
                    </span>
                  </div>
                  {log.fatigue_level && (
                    <div className="text-right">
                      <p className="text-sm text-gray-500">Fatigue</p>
                      <p className="text-xl font-bold text-gray-900">{log.fatigue_level}/10</p>
                    </div>
                  )}
                </div>

                {log.free_text_reflection && (
                  <p className="mt-3 text-gray-600 text-sm">{log.free_text_reflection}</p>
                )}

                {log.ai_analysis && (
                  <div className="mt-4 p-4 bg-green-50 rounded-md">
                    <p className="text-sm font-medium text-green-900">AI Insight</p>
                    <p className="text-sm text-green-800 mt-1">{log.ai_analysis.human_insight}</p>
                  </div>
                )}

                <div className="mt-4 flex space-x-2">
                  <a
                    href={`/log?date=${log.date}`}
                    className="text-sm text-blue-600 hover:text-blue-800"
                  >
                    View Details
                  </a>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
