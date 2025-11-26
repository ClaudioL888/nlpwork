import { ChatMessage } from "../../types/chat";

interface Props {
  messages: ChatMessage[];
  currentUser: string;
}

const sentimentStyles: Record<string, string> = {
  positive: "bg-emerald-500/15 border-emerald-400/40",
  neutral: "bg-slate-600/20 border-slate-500/40",
  negative: "bg-rose-500/15 border-rose-400/40"
};

export function MessageList({ messages, currentUser }: Props) {
  return (
    <div className="space-y-3">
      {messages.map((message) => (
        <div
          key={`${message.created_at}-${message.user_id}-${message.text}`}
          className={`rounded-lg border p-3 text-sm ${sentimentStyles[message.sentiment] ?? "border-slate-600"}`}
        >
          <div className="flex items-center justify-between text-xs text-slate-300">
            <span className={message.user_id === currentUser ? "text-primary font-semibold" : "text-slate-200"}>{message.user_id}</span>
            <span>{new Date(message.created_at).toLocaleTimeString()}</span>
          </div>
          <p className="mt-2 text-white">{message.text}</p>
          <div className="mt-2 flex justify-between text-xs text-slate-400">
            <span>情绪：{message.sentiment}</span>
            <span>风险 {(message.crisis_probability * 100).toFixed(0)}%</span>
          </div>
        </div>
      ))}
      {!messages.length && <p className="text-sm text-slate-400">暂无消息，开始对话吧。</p>}
    </div>
  );
}
