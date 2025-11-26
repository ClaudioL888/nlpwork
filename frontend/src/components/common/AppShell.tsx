import { PropsWithChildren } from "react";

interface Props extends PropsWithChildren {
  theme: "light" | "dark";
}

export function AppShell({ theme, children }: Props) {
  return (
    <div className="min-h-screen text-slate-100">
      <header className="border-b border-slate-800/60 bg-slate-900/70 backdrop-blur px-6 py-4 flex items-center justify-between">
        <div className="space-y-1">
          <p className="text-xs uppercase tracking-widest text-slate-400">Digital Empathy Platform</p>
          <h1 className="text-2xl font-semibold">数字共情中台 · 实时洞察</h1>
          <p className="text-sm text-slate-400">看板 · 聊天 · 检索，一站式情绪与风险监测</p>
        </div>
        <span className="text-sm px-3 py-1 rounded-full bg-slate-800 text-slate-300 border border-slate-700">
          主题：{theme === "dark" ? "深色" : "浅色"}
        </span>
      </header>
      <main className="px-6 py-6 space-y-4 max-w-7xl mx-auto">{children}</main>
    </div>
  );
}
