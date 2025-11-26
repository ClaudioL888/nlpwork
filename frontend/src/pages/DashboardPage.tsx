import { useMemo } from "react";
import { KeywordForm } from "../components/dashboard/KeywordForm";
import { EmotionTrendChart } from "../components/dashboard/EmotionTrendChart";
import { RiskSummaryCard } from "../components/dashboard/RiskSummaryCard";
import { RepresentativeQuotes } from "../components/dashboard/RepresentativeQuotes";
import { LoadingState } from "../components/common/LoadingState";
import { ErrorBanner } from "../components/common/ErrorBanner";
import { useDashboardState } from "../store/dashboardState";

export function DashboardPage() {
  const { data, loading, error, keyword, hours, analyze, setKeyword, setHours } = useDashboardState();

  const handleSubmit = (keyword: string, selectedHours: number) => {
    setKeyword(keyword);
    setHours(selectedHours);
    analyze(keyword, selectedHours);
  };

  const firstLoad = !data && !loading;
  const quotes = useMemo(() => data?.representative_quotes ?? [], [data]);

  return (
    <div className="space-y-6">
      <KeywordForm keyword={keyword} hours={hours} loading={loading} onSubmit={handleSubmit} />
      {error && <ErrorBanner message={error} />}
      {firstLoad && <LoadingState label="等待关键词输入" />}
      {data && (
        <div className="grid gap-4 lg:grid-cols-3">
          <div className="lg:col-span-2 space-y-4">
            <EmotionTrendChart data={data.emotion_series} />
            <RepresentativeQuotes quotes={quotes} />
          </div>
          <RiskSummaryCard summary={data.crisis_summary} />
        </div>
      )}
    </div>
  );
}
