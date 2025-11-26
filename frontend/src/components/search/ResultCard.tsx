import { SearchResultItem } from "../../types/search";

interface Props {
  item: SearchResultItem;
}

const riskColor: Record<string, string> = {
  high: "text-red-400",
  medium: "text-yellow-400",
  low: "text-green-400"
};

export function ResultCard({ item }: Props) {
  return (
    <div className="rounded-lg border border-slate-800 bg-slate-900/60 p-4 shadow-inner shadow-black/20">
      <div className="flex justify-between text-sm text-slate-300">
        <div>
          <p className="text-xs uppercase text-slate-500">关键词</p>
          <p className="text-lg font-semibold text-white capitalize">{item.keyword}</p>
        </div>
        <span className={`text-sm font-semibold ${riskColor[item.risk_level] ?? "text-slate-200"}`}>
          {item.risk_level.toUpperCase()}
        </span>
      </div>
      <p className="mt-3 text-sm text-slate-400">
        {new Date(item.window_start).toLocaleString()} → {new Date(item.window_end).toLocaleString()}
      </p>
      {item.representative_quote && (
        <blockquote className="mt-3 border-l-2 border-slate-600 pl-3 text-white">{item.representative_quote}</blockquote>
      )}
      <div className="mt-3 grid grid-cols-3 text-xs text-slate-400">
        {Object.entries(item.emotion_distribution).map(([label, value]) => (
          <div key={label}>
            <p className="uppercase tracking-wide">{label}</p>
            <p className="text-white">{(value * 100).toFixed(1)}%</p>
          </div>
        ))}
      </div>
    </div>
  );
}
