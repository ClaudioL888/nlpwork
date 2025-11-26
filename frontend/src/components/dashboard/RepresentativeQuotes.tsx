import { RepresentativeQuote } from "../../hooks/useEventAnalysis";

interface Props {
  quotes: RepresentativeQuote[];
}

const sentimentPalette: Record<string, string> = {
  positive: "text-success",
  negative: "text-danger",
  neutral: "text-slate-300"
};

export function RepresentativeQuotes({ quotes }: Props) {
  if (!quotes.length) {
    return <p className="text-sm text-slate-400">暂无代表语句。</p>;
  }
  return (
    <div className="space-y-3">
      {quotes.map((quote) => (
        <div key={quote.timestamp + quote.text} className="rounded-lg border border-slate-800 bg-slate-900/60 p-3 shadow-inner shadow-black/20">
          <p className="text-sm text-white leading-relaxed">{quote.text}</p>
          <div className="mt-2 flex items-center justify-between text-xs text-slate-400">
            <span className={sentimentPalette[quote.label] ?? "text-slate-200"}>情绪：{quote.label}</span>
            <span>风险：{(quote.crisis_probability * 100).toFixed(0)}%</span>
          </div>
        </div>
      ))}
    </div>
  );
}
