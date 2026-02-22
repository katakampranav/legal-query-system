"use client";

import { useCallback, useRef, useState } from "react";
import { sendMessage } from "../services/legalq-api";
import type { ChatMode, Message } from "../types/chat-types";

function generateId(): string {
  return `${Date.now()}-${Math.random().toString(36).slice(2, 9)}`;
}

export function useChat() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [mode, setMode] = useState<ChatMode>("normal");
  const abortRef = useRef<AbortController | null>(null);

  const sendUserMessage = useCallback(
    async (question: string) => {
      if (!question.trim() || isLoading) return;

      const userMessage: Message = {
        id: generateId(),
        role: "user",
        content: question.trim(),
        timestamp: new Date(),
      };

      setMessages((prev) => [...prev, userMessage]);
      setIsLoading(true);
      setError(null);

      try {
        const answer = await sendMessage(question.trim(), mode);

        const assistantMessage: Message = {
          id: generateId(),
          role: "assistant",
          content: answer,
          timestamp: new Date(),
        };

        setMessages((prev) => [...prev, assistantMessage]);
      } catch (err: unknown) {
        const errorMessage =
          err instanceof Error
            ? err.message
            : "Something went wrong. Please try again.";
        setError(errorMessage);

        const errorBubble: Message = {
          id: generateId(),
          role: "assistant",
          content:
            "I'm sorry, I encountered an error while processing your question. Please try again.",
          timestamp: new Date(),
        };
        setMessages((prev) => [...prev, errorBubble]);
      } finally {
        setIsLoading(false);
      }
    },
    [isLoading, mode]
  );

  const clearChat = useCallback(() => {
    setMessages([]);
    setError(null);
  }, []);

  return {
    messages,
    isLoading,
    error,
    mode,
    setMode,
    sendUserMessage,
    clearChat,
  };
}
