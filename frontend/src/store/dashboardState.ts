import { create } from "zustand";
import { apiClient } from "../api/client";
import type { EventInsightResponse } from "../hooks/useEventAnalysis";

interface DashboardState {
  keyword: string;
  hours: number;
  data: EventInsightResponse | null;
  loading: boolean;
  error: string | null;
  setKeyword: (value: string) => void;
  setHours: (value: number) => void;
  analyze: (keyword?: string, hours?: number) => Promise<void>;
}

export const useDashboardState = create<DashboardState>((set, get) => ({
  keyword: "earthquake",
  hours: 24,
  data: null,
  loading: false,
  error: null,
  setKeyword: (value) => set({ keyword: value }),
  setHours: (value) => set({ hours: value }),
  analyze: async (keywordInput?: string, hoursInput?: number) => {
    const keyword = (keywordInput ?? get().keyword).trim();
    const hours = hoursInput ?? get().hours;
    if (!keyword) {
      set({ error: "Keyword is required" });
      return;
    }
    set({ loading: true, error: null, keyword, hours });
    try {
      const response = await apiClient.post<EventInsightResponse>("/analyze_event", { keyword, hours });
      set({ data: response.data });
    } catch (err) {
      set({ error: (err as Error).message, data: null });
    } finally {
      set({ loading: false });
    }
  }
}));
