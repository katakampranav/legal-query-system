"use client";

import { cn } from "@/lib/utils";
import { Scale, User } from "lucide-react";
import ReactMarkdown from "react-markdown";
import type { Message } from "../types/chat-types";

interface MessageBubbleProps {
  message: Message;
}

function TypingDots() {
  return (
    <span className="inline-flex items-end gap-1 h-4">
      <span
        className="w-1.5 h-1.5 rounded-full bg-muted-foreground animate-bounce"
        style={{ animationDelay: "0ms" }}
      />
      <span
        className="w-1.5 h-1.5 rounded-full bg-muted-foreground animate-bounce"
        style={{ animationDelay: "150ms" }}
      />
      <span
        className="w-1.5 h-1.5 rounded-full bg-muted-foreground animate-bounce"
        style={{ animationDelay: "300ms" }}
      />
    </span>
  );
}

export function MessageBubble({ message }: MessageBubbleProps) {
  const isUser = message.role === "user";

  return (
    <div
      className={cn(
        "flex items-start gap-3 w-full",
        isUser ? "flex-row-reverse" : "flex-row",
      )}
    >
      {/* Avatar */}
      <div
        className={cn(
          "flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center shadow-sm",
          isUser
            ? "bg-gradient-to-br from-primary to-[#b85d38] text-white"
            : "bg-muted text-muted-foreground border border-border",
        )}
      >
        {isUser ? <User size={15} /> : <Scale size={15} />}
      </div>

      {/* Bubble */}
      <div
        className={cn(
          "max-w-[75%] rounded-2xl px-4 py-3 text-sm leading-relaxed shadow-sm",
          isUser
            ? "bg-gradient-to-br from-primary to-[#b85d38] text-white rounded-tr-sm"
            : "bg-background border border-border text-foreground rounded-tl-sm",
        )}
      >
        <div className="prose prose-sm dark:prose-invert max-w-none prose-headings:font-semibold prose-headings:margin-top-3 prose-headings:margin-bottom-2 prose-p:margin-1 prose-ul:margin-1 prose-ol:margin-1 prose-li:margin-0">
          <ReactMarkdown
            components={{
              h1: ({ ...props }) => (
                <h1 className="text-base font-bold mt-3 mb-2" {...props} />
              ),
              h2: ({ ...props }) => (
                <h2 className="text-base font-bold mt-3 mb-2" {...props} />
              ),
              h3: ({ ...props }) => (
                <h3 className="text-sm font-bold mt-2 mb-1" {...props} />
              ),
              ul: ({ ...props }) => (
                <ul className="list-disc list-inside space-y-1" {...props} />
              ),
              ol: ({ ...props }) => (
                <ol className="list-decimal list-inside space-y-1" {...props} />
              ),
              li: ({ ...props }) => <li className="ml-2" {...props} />,
              strong: ({ ...props }) => (
                <strong className="font-bold" {...props} />
              ),
              em: ({ ...props }) => <em className="italic" {...props} />,
              code: ({ ...props }) => (
                <code
                  className={cn(
                    "px-1.5 py-0.5 rounded text-xs font-mono",
                    isUser
                      ? "bg-white/20 text-white"
                      : "bg-muted text-foreground",
                  )}
                  {...props}
                />
              ),
              p: ({ ...props }) => <p className="mb-2 last:mb-0" {...props} />,
            }}
          >
            {message.content}
          </ReactMarkdown>
        </div>
        <p
          className={cn(
            "text-[10px] mt-2 text-right",
            isUser ? "text-white/60" : "text-muted-foreground",
          )}
        >
          {message.timestamp.toLocaleTimeString([], {
            hour: "2-digit",
            minute: "2-digit",
          })}
        </p>
      </div>
    </div>
  );
}

export function ThinkingBubble() {
  return (
    <div className="flex items-start gap-3 w-full flex-row">
      <div className="flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center bg-muted text-muted-foreground border border-border shadow-sm">
        <Scale size={15} />
      </div>
      <div className="bg-background border border-border rounded-2xl rounded-tl-sm px-4 py-3 shadow-sm">
        <div className="flex items-center gap-2 text-sm text-muted-foreground">
          <TypingDots />
          <span className="text-xs">Thinking...</span>
        </div>
      </div>
    </div>
  );
}
