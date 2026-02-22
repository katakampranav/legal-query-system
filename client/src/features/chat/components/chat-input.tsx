"use client";

import { useCallback, useRef, useState } from "react";
import { Textarea } from "@/components/ui/textarea";
import { Button } from "@/components/ui/button";
import { SendHorizonal } from "lucide-react";

interface ChatInputProps {
    onSend: (message: string) => void;
    isLoading: boolean;
}

export function ChatInput({ onSend, isLoading }: ChatInputProps) {
    const [value, setValue] = useState("");
    const textareaRef = useRef<HTMLTextAreaElement>(null);

    const handleSend = useCallback(() => {
        const trimmed = value.trim();
        if (!trimmed || isLoading) return;
        onSend(trimmed);
        setValue("");
        if (textareaRef.current) {
            textareaRef.current.style.height = "auto";
        }
    }, [value, isLoading, onSend]);

    const handleKeyDown = useCallback(
        (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
            if (e.key === "Enter" && !e.shiftKey) {
                e.preventDefault();
                handleSend();
            }
        },
        [handleSend]
    );

    const handleChange = useCallback((e: React.ChangeEvent<HTMLTextAreaElement>) => {
        setValue(e.target.value);
        e.target.style.height = "auto";
        e.target.style.height = `${Math.min(e.target.scrollHeight, 160)}px`;
    }, []);

    return (
        <div className="flex items-end gap-3 w-full">
            <div className="flex-1 relative">
                <Textarea
                    ref={textareaRef}
                    value={value}
                    onChange={handleChange}
                    onKeyDown={handleKeyDown}
                    placeholder="Describe your situation or ask a legal question..."
                    disabled={isLoading}
                    className="min-h-[52px] max-h-40 py-3.5 text-sm leading-relaxed bg-background text-foreground border-border placeholder:text-muted-foreground"
                    rows={1}
                />
            </div>
            <Button
                onClick={handleSend}
                disabled={!value.trim() || isLoading}
                size="icon"
                className="h-[52px] w-[52px] rounded-xl flex-shrink-0 shadow-md"
                aria-label="Send message"
            >
                <SendHorizonal size={18} />
            </Button>
        </div>
    );
}
