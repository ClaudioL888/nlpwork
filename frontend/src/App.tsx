import { useEffect, useState } from "react";
import { useAppState } from "./store/appState";
import { AppShell } from "./components/common/AppShell";
import { ErrorBanner } from "./components/common/ErrorBanner";
import { LoadingState } from "./components/common/LoadingState";
import { DashboardPage } from "./pages/DashboardPage";
import { ChatPage } from "./pages/ChatPage";
import { SearchPage } from "./pages/SearchPage";

function App() {
  const { theme, initialize, initialized, error } = useAppState();
  const [view, setView] = useState<"dashboard" | "chat" | "search">("dashboard");

  useEffect(() => {
    initialize();
  }, [initialize]);

  return (
    <AppShell theme={theme}>
      {error && <ErrorBanner message={error} />}
      <div className="flex gap-3 text-sm">
        {[
          { id: "dashboard", label: "总览看板" },
          { id: "chat", label: "实时聊天" },
          { id: "search", label: "事件检索" }
        ].map((tab) => (
          <button
            key={tab.id}
            className={`rounded-full px-4 py-2 transition ${
              view === tab.id ? "bg-primary text-white shadow-lg shadow-primary/30" : "bg-slate-800 text-slate-300 hover:bg-slate-700"
            }`}
            onClick={() => setView(tab.id as typeof view)}
          >
            {tab.label}
          </button>
        ))}
      </div>
      {!initialized ? (
        <LoadingState label="Initializing SDK" />
      ) : view === "dashboard" ? (
        <DashboardPage />
      ) : view === "chat" ? (
        <ChatPage />
      ) : (
        <SearchPage />
      )}
    </AppShell>
  );
}

export default App;
