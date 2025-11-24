import { FormEvent, useState } from "react";

interface Props {
  keyword: string;
  loading: boolean;
  onSubmit: (nextKeyword: string) => void;
}

export function SearchBar({ keyword, loading, onSubmit }: Props) {
  const [value, setValue] = useState(keyword);

  const handleSubmit = (event: FormEvent) => {
    event.preventDefault();
    if (!value.trim()) return;
    onSubmit(value.trim());
  };

  return (
    <form onSubmit={handleSubmit} className="flex flex-col gap-3 md:flex-row">
      <input
        value={value}
        onChange={(event) => setValue(event.target.value)}
        className="flex-1 rounded-md border border-slate-600 bg-slate-900 px-3 py-2 text-white focus:outline-primary"
        placeholder="Search events"
      />
      <button
        type="submit"
        disabled={loading}
        className="h-10 rounded-md bg-primary px-6 text-sm font-semibold text-white disabled:opacity-60"
      >
        {loading ? "Searching..." : "Search"}
      </button>
    </form>
  );
}
