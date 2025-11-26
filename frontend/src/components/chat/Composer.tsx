import { FormEvent, useState } from "react";

interface Props {
  onSend: (text: string) => void;
  disabled?: boolean;
}

export function Composer({ onSend, disabled }: Props) {
  const [text, setText] = useState("");

  const handleSubmit = (event: FormEvent) => {
    event.preventDefault();
    if (!text.trim()) return;
    onSend(text.trim());
    setText("");
  };

  return (
    <form onSubmit={handleSubmit} className="flex gap-3">
      <input
        value={text}
        onChange={(event) => setText(event.target.value)}
        className="flex-1 rounded-md border border-slate-700 bg-slate-950/60 px-3 py-2 text-white focus:outline-primary focus:ring-2 focus:ring-primary/50"
        placeholder="输入想法，回车发送…"
        disabled={disabled}
      />
      <button
        type="submit"
        disabled={disabled}
        className="rounded-md bg-primary px-5 py-2 text-sm font-semibold text-white disabled:opacity-60"
      >
        Send
      </button>
    </form>
  );
}
