interface Props {
  sort: "risk" | "heat";
  onChange: (sort: "risk" | "heat") => void;
}

export function ResultFilters({ sort, onChange }: Props) {
  return (
    <div className="flex items-center gap-3 text-sm text-slate-300">
      <label className="flex items-center gap-2">
        Sort by
        <select
          value={sort}
          onChange={(event) => onChange(event.target.value as "risk" | "heat")}
          className="rounded-md border border-slate-600 bg-slate-900 px-3 py-2 text-white"
        >
          <option value="risk">Risk</option>
          <option value="heat">Heat</option>
        </select>
      </label>
    </div>
  );
}
