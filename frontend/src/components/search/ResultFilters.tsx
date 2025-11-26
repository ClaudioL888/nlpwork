interface Props {
  sort: "risk" | "heat";
  onChange: (sort: "risk" | "heat") => void;
}

export function ResultFilters({ sort, onChange }: Props) {
  return (
    <div className="flex items-center gap-3 text-sm text-slate-300">
      <label className="flex items-center gap-2">
        排序
        <select
          value={sort}
          onChange={(event) => onChange(event.target.value as "risk" | "heat")}
          className="rounded-md border border-slate-700 bg-slate-950/60 px-3 py-2 text-white"
        >
          <option value="risk">风险</option>
          <option value="heat">热度</option>
        </select>
      </label>
    </div>
  );
}
