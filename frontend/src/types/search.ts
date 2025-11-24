export interface SearchResultItem {
  keyword: string;
  window_start: string;
  window_end: string;
  risk_level: string;
  emotion_distribution: Record<string, number>;
  representative_quote?: string | null;
}

export interface SearchResponse {
  total: number;
  page: number;
  page_size: number;
  results: SearchResultItem[];
}
