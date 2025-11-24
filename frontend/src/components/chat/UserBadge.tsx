interface Props {
  userId: string;
  status: "connecting" | "open" | "closed";
}

const statusText: Record<Props["status"], string> = {
  connecting: "Connecting...",
  open: "Online",
  closed: "Disconnected"
};

const statusColor: Record<Props["status"], string> = {
  connecting: "bg-yellow-400",
  open: "bg-green-400",
  closed: "bg-red-400"
};

export function UserBadge({ userId, status }: Props) {
  return (
    <div className="flex items-center gap-3 rounded-md border border-slate-700/40 bg-slate-900/40 px-4 py-2 text-sm text-slate-300">
      <span className="font-mono text-white">{userId}</span>
      <span className={`flex items-center gap-2 text-xs ${status === "closed" ? "text-red-400" : "text-slate-400"}`}>
        <span className={`h-2 w-2 rounded-full ${statusColor[status]}`} />
        {statusText[status]}
      </span>
    </div>
  );
}
