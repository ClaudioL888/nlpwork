export interface ChatMessage {
  room_id: string;
  user_id: string;
  text: string;
  sentiment: string;
  crisis_probability: number;
  created_at: string;
}
