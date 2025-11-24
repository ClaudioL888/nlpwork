import { FormEvent, useState } from "react";

interface Props {
  keyword: string;
  hours: number;
  loading: boolean;
  onSubmit: (keyword: string, hours: number) => void;
}

export function KeywordForm({ keyword, hours, loading, onSubmit }: Props) {
  const [localKeyword, setLocalKeyword] = useState(keyword);
  const [localHours, setLocalHours] = useState(hours);

  const handleSubmit = (event: FormEvent) => {
    event.preventDefault();
    if (!localKeyword.trim()) {
      return;
    }
    onSubmit(localKeyword.trim(), localHours);
  };

  return (
    <form onSubmit={handleSubmit} className="flex flex-col gap-3 md:flex-row md:items-end">
      <label className="flex-1 text-sm">
        <span className="mb-1 block text-slate-400">Keyword</span>
        <input
          value={localKeyword}
          onChange={(event) => setLocalKeyword(event.target.value)}
          className="w-full rounded-md border border-slate-600 bg-slate-900 px-3 py-2 text-white focus:outline-primary"
          placeholder="e.g., earthquake"
        />
      </label>
      <label className="text-sm">
        <span className="mb-1 block text-slate-400">Hours</span>
        <input
          value={localHours}
          onChange={(event) => setLocalHours(Number(event.target.value))}
          type="number"
          min={1}
          max={72}
          className="w-32 rounded-md border border-slate-600 bg-slate-900 px-3 py-2 text-white focus:outline-primary"
        />
      </label>
      <button
        type="submit"
        disabled={loading}
        className="h-10 rounded-md bg-primary px-6 text-sm font-semibold text-white disabled:opacity-60"
      >
        {loading ? "Analyzing..." : "Analyze"}
      </button>
    </form>
  );
}
