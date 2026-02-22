"use client";

import { useEffect, useRef } from "react";
import { MessageBubble, ThinkingBubble } from "./message-bubble";
import { Scale } from "lucide-react";
import type { Message } from "../types/chat-types";

interface MessageListProps {
    messages: Message[];
    isLoading: boolean;
}

export function MessageList({ messages, isLoading }: MessageListProps) {
    const bottomRef = useRef<HTMLDivElement>(null);

    useEffect(() => {
        bottomRef.current?.scrollIntoView({ behavior: "smooth" });
    }, [messages, isLoading]);

    if (messages.length === 0 && !isLoading) {
        return (
            <div className="flex-1 flex items-center justify-center px-4">
                <div className="text-center max-w-sm">
                    <div className="w-16 h-16 bg-accent rounded-2xl flex items-center justify-center mx-auto mb-4">
                        <Scale size={32} className="text-primary" />
                    </div>
                    <h3 className="text-foreground font-semibold text-lg mb-1">
                        Ask LegalQ anything
                    </h3>
                    <p className="text-muted-foreground text-sm">
                        Describe your situation and get clear legal explanations based on
                        Indian criminal law (BNS).
                    </p>
                </div>
            </div>
        );
    }

    return (
        <div className="flex-1 overflow-y-auto px-4 py-6 space-y-4">
            {messages.map((message) => (
                <MessageBubble key={message.id} message={message} />
            ))}
            {isLoading && <ThinkingBubble />}
            <div ref={bottomRef} />
        </div>
    );
}
