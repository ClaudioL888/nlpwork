import { create } from "zustand";
import { apiClient } from "../api/client";
import type { SearchResponse } from "../types/search";

interface SearchState {
  keyword: string;
  page: number;
  sort: "risk" | "heat";
  loading: boolean;
  error: string | null;
  results: SearchResponse | null;
  setKeyword: (value: string) => void;
  setSort: (value: "risk" | "heat") => void;
  setPage: (value: number) => void;
  search: (override?: { keyword?: string; page?: number; sort?: "risk" | "heat" }) => Promise<void>;
}

export const useSearchState = create<SearchState>((set, get) => ({
  keyword: "earthquake",
  page: 1,
  sort: "risk",
  loading: false,
  error: null,
  results: null,
  setKeyword: (value) => set({ keyword: value }),
  setSort: (value) => set({ sort: value }),
  setPage: (value) => set({ page: value }),
  search: async (override) => {
    const keyword = override?.keyword ?? get().keyword;
    const page = override?.page ?? get().page;
    const sort = override?.sort ?? get().sort;
    set({ keyword, page, sort, loading: true, error: null });
    try {
      const response = await apiClient.post<SearchResponse>("/search", { keyword, page, sort });
      set({ results: response.data });
    } catch (err) {
      set({ error: (err as Error).message, results: null });
    } finally {
      set({ loading: false });
    }
  },
}));
