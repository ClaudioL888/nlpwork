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
    return <p className="text-sm text-slate-400">No representative quotes yet.</p>;
  }
  return (
    <div className="space-y-3">
      {quotes.map((quote) => (
        <div key={quote.timestamp + quote.text} className="rounded-md border border-slate-700/40 bg-slate-900/40 p-3">
          <p className="text-sm text-white">{quote.text}</p>
          <div className="mt-2 flex items-center justify-between text-xs text-slate-400">
            <span className={sentimentPalette[quote.label] ?? "text-slate-200"}>Label: {quote.label}</span>
            <span>Risk: {(quote.crisis_probability * 100).toFixed(0)}%</span>
          </div>
        </div>
      ))}
    </div>
  );
}
