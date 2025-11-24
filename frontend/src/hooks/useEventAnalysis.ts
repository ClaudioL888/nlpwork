import { useCallback, useState } from "react";
import { apiClient } from "../api/client";

export interface EmotionPoint {
  timestamp: string;
  positive: number;
  neutral: number;
  negative: number;
}

export interface CrisisSummary {
  max_probability: number;
  avg_probability: number;
  high_risk_count: number;
}

export interface RepresentativeQuote {
  text: string;
  label: string;
  crisis_probability: number;
  timestamp: string;
}

export interface EventInsightResponse {
  keyword: string;
  window_start: string;
  window_end: string;
  emotion_series: EmotionPoint[];
  crisis_summary: CrisisSummary;
  representative_quotes: RepresentativeQuote[];
  network_graph: { nodes: Array<{ id: string; label: string; size: number }>; edges: Array<{ source: string; target: string }> };
}

export function useEventAnalysis() {
  const [data, setData] = useState<EventInsightResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const analyze = useCallback(async (keyword: string, hours = 6) => {
    setLoading(true);
    setError(null);
    try {
      const response = await apiClient.post<EventInsightResponse>("/analyze_event", {
        keyword,
        hours
      });
      setData(response.data);
    } catch (err) {
      setError((err as Error).message);
    } finally {
      setLoading(false);
    }
  }, []);

  return { data, loading, error, analyze };
}
