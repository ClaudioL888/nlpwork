import { PropsWithChildren } from "react";

interface Props extends PropsWithChildren {
  theme: "light" | "dark";
}

export function AppShell({ theme, children }: Props) {
  return (
    <div className={theme === "dark" ? "bg-surface text-white min-h-screen" : "bg-white text-slate-900 min-h-screen"}>
      <header className="border-b border-slate-700/40 px-6 py-4 flex items-center justify-between">
        <div>
          <p className="text-xs uppercase tracking-widest text-slate-400">Digital Empathy Platform</p>
          <h1 className="text-xl font-semibold">Foundation UI</h1>
        </div>
        <span className="text-sm text-slate-400">Theme: {theme}</span>
      </header>
      <main className="px-6 py-6 space-y-4">{children}</main>
    </div>
  );
}
