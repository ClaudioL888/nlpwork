import { CrisisSummary } from "../../hooks/useEventAnalysis";

interface Props {
  summary: CrisisSummary;
}

export function RiskSummaryCard({ summary }: Props) {
  return (
    <div className="rounded-lg border border-slate-700/40 bg-slate-900/40 p-4">
      <h3 className="mb-2 text-sm uppercase tracking-wide text-slate-400">Crisis Summary</h3>
      <div className="flex gap-4 text-sm">
        <div>
          <p className="text-slate-400">Max Probability</p>
          <p className="text-2xl font-semibold text-danger">{(summary.max_probability * 100).toFixed(1)}%</p>
        </div>
        <div>
          <p className="text-slate-400">Average Probability</p>
          <p className="text-2xl font-semibold text-accent">{(summary.avg_probability * 100).toFixed(1)}%</p>
        </div>
        <div>
          <p className="text-slate-400">High Risk Count</p>
          <p className="text-2xl font-semibold text-white">{summary.high_risk_count}</p>
        </div>
      </div>
    </div>
  );
}
