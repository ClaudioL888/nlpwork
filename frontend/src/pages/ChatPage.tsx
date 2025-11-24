import { useCallback, useMemo, useState } from "react";
import { useChatSocket } from "../hooks/useChatSocket";
import { ChatMessage } from "../types/chat";
import { MessageList } from "../components/chat/MessageList";
import { Composer } from "../components/chat/Composer";
import { UserBadge } from "../components/chat/UserBadge";
import { ErrorBanner } from "../components/common/ErrorBanner";

const randomUser = () => `user-${Math.random().toString(36).slice(2, 7)}`;

export function ChatPage() {
  const [roomId] = useState("global");
  const [userId] = useState(randomUser);
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [error, setError] = useState<string | null>(null);

  const handleIncoming = useCallback((payload: ChatMessage | { type: string; code?: string }) => {
    if ("type" in payload && payload.type === "error") {
      setError(payload.code ?? "Error");
      return;
    }
    setMessages((prev) => [...prev, payload as ChatMessage]);
  }, []);

  const { send, status } = useChatSocket(roomId, userId, handleIncoming);

  const sortedMessages = useMemo(() => messages.sort((a, b) => a.created_at.localeCompare(b.created_at)), [messages]);

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-xs uppercase tracking-wider text-slate-400">Room</p>
          <p className="text-lg font-semibold text-white">{roomId}</p>
        </div>
        <UserBadge userId={userId} status={status} />
      </div>
      {error && <ErrorBanner message={error} />}
      <div className="rounded-lg border border-slate-700/40 bg-slate-900/40 p-4">
        <MessageList messages={sortedMessages} currentUser={userId} />
      </div>
      <Composer onSend={send} disabled={status !== "open"} />
    </div>
  );
}
