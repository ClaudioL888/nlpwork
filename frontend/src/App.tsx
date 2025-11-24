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
          { id: "dashboard", label: "Dashboard" },
          { id: "chat", label: "Chat" },
          { id: "search", label: "Search" }
        ].map((tab) => (
          <button
            key={tab.id}
            className={`rounded-md px-4 py-2 ${view === tab.id ? "bg-primary text-white" : "bg-slate-800 text-slate-300"}`}
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
