interface Props {
  page: number;
  pageSize: number;
  total: number;
  onChange: (page: number) => void;
}

export function Pagination({ page, pageSize, total, onChange }: Props) {
  const totalPages = Math.max(1, Math.ceil(total / pageSize));
  const prevDisabled = page <= 1;
  const nextDisabled = page >= totalPages;

  return (
    <div className="flex items-center gap-3 text-sm text-slate-300">
      <button
        className="rounded-md border border-slate-600 px-3 py-1 disabled:opacity-50"
        disabled={prevDisabled}
        onClick={() => onChange(page - 1)}
      >
        上一页
      </button>
      <span>
        第 {page} / {totalPages} 页
      </span>
      <button
        className="rounded-md border border-slate-600 px-3 py-1 disabled:opacity-50"
        disabled={nextDisabled}
        onClick={() => onChange(page + 1)}
      >
        下一页
      </button>
    </div>
  );
}
