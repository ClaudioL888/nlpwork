import { useCallback, useState } from "react";
import { apiClient } from "../api/client";
import { SearchResponse } from "../types/search";

export function useSearch(initialKeyword = "earthquake") {
  const [keyword, setKeyword] = useState(initialKeyword);
  const [page, setPage] = useState(1);
  const [sort, setSort] = useState<"risk" | "heat">("risk");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [results, setResults] = useState<SearchResponse | null>(null);

  const search = useCallback(
    async (override?: { keyword?: string; page?: number; sort?: "risk" | "heat" }) => {
      const nextKeyword = override?.keyword ?? keyword;
      const nextPage = override?.page ?? page;
      const nextSort = override?.sort ?? sort;

      setKeyword(nextKeyword);
      setPage(nextPage);
      setSort(nextSort);
      setLoading(true);
      setError(null);

      try {
        const response = await apiClient.post<SearchResponse>("/search", {
          keyword: nextKeyword,
          page: nextPage,
          sort: nextSort
        });
        setResults(response.data);
      } catch (err) {
        setError((err as Error).message);
      } finally {
        setLoading(false);
      }
    },
    [keyword, page, sort]
  );

  return { keyword, page, sort, loading, error, results, search };
}
