import { useEffect, useRef, useState } from "react";

export type SocketStatus = "connecting" | "open" | "closed";

export function useChatSocket(roomId: string, userId: string, onMessage: (payload: any) => void) {
  const socketRef = useRef<WebSocket | null>(null);
  const [status, setStatus] = useState<SocketStatus>("connecting");

  useEffect(() => {
    const url = new URL(`/ws/chat`, window.location.origin.replace("http", "ws"));
    url.searchParams.set("room_id", roomId);
    url.searchParams.set("user_id", userId);
    const socket = new WebSocket(url.toString());
    socketRef.current = socket;
    setStatus("connecting");

    socket.onopen = () => setStatus("open");
    socket.onclose = () => setStatus("closed");
    socket.onerror = () => setStatus("closed");
    socket.onmessage = (event) => {
      const data = JSON.parse(event.data);
      onMessage(data);
    };

    return () => {
      socket.close();
    };
  }, [roomId, userId, onMessage]);

  return {
    status,
    send: (text: string) => {
      if (!text.trim()) return;
      socketRef.current?.send(JSON.stringify({ text }));
    }
  };
}
