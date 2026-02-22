export type ChatMode = "normal" | "lawyer";

export type MessageRole = "user" | "assistant";

export interface Message {
  id: string;
  role: MessageRole;
  content: string;
  timestamp: Date;
}

export interface AskRequest {
  question: string;
  mode: ChatMode;
}

export interface AskResponse {
  answer: string;
  citations?: string[];
  mode: string;
  session_id?: string;
}

export interface ChatState {
  messages: Message[];
  isLoading: boolean;
  error: string | null;
  mode: ChatMode;
}
