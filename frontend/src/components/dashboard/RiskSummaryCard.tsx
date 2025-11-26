import { CrisisSummary } from "../../hooks/useEventAnalysis";

interface Props {
  summary: CrisisSummary;
}

export function RiskSummaryCard({ summary }: Props) {
  return (
    <div className="rounded-xl border border-slate-800 bg-slate-900/60 p-4 shadow-inner shadow-black/20">
      <h3 className="mb-3 text-sm uppercase tracking-wide text-slate-300">危机概览</h3>
      <div className="flex gap-6 text-sm">
        <div className="space-y-1">
          <p className="text-slate-400">最高风险</p>
          <p className="text-2xl font-semibold text-danger">{(summary.max_probability * 100).toFixed(1)}%</p>
        </div>
        <div className="space-y-1">
          <p className="text-slate-400">平均风险</p>
          <p className="text-2xl font-semibold text-accent">{(summary.avg_probability * 100).toFixed(1)}%</p>
        </div>
        <div className="space-y-1">
          <p className="text-slate-400">高风险条数</p>
          <p className="text-2xl font-semibold text-white">{summary.high_risk_count}</p>
        </div>
      </div>
    </div>
  );
}
