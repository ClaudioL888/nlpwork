import { useEffect } from "react";
import { SearchBar } from "../components/search/SearchBar";
import { ResultFilters } from "../components/search/ResultFilters";
import { Pagination } from "../components/search/Pagination";
import { ResultCard } from "../components/search/ResultCard";
import { useSearch } from "../hooks/useSearch";
import { LoadingState } from "../components/common/LoadingState";
import { ErrorBanner } from "../components/common/ErrorBanner";

export function SearchPage() {
  const { keyword, page, sort, loading, error, results, search } = useSearch();

  useEffect(() => {
    search();
  }, []); // eslint-disable-line react-hooks/exhaustive-deps

  return (
    <div className="space-y-4">
      <SearchBar keyword={keyword} loading={loading} onSubmit={(nextKeyword) => search({ keyword: nextKeyword, page: 1 })} />
      <div className="flex flex-col gap-3 md:flex-row md:items-center md:justify-between">
        <ResultFilters sort={sort} onChange={(nextSort) => search({ sort: nextSort, page: 1 })} />
        {results && (
          <Pagination
            page={results.page}
            pageSize={results.page_size}
            total={results.total}
            onChange={(nextPage) => search({ page: nextPage })}
          />
        )}
      </div>
      {error && <ErrorBanner message={error} />}
      {loading && <LoadingState label="Searching" />}
      <div className="grid gap-3">
        {results?.results.map((item) => (
          <ResultCard key={`${item.keyword}-${item.window_start}`} item={item} />
        ))}
        {!loading && !results?.results.length && <p className="text-sm text-slate-400">No results found.</p>}
      </div>
    </div>
  );
}
