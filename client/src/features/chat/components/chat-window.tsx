"use client";

import { useChat } from "../hooks/use-chat";
import { MessageList } from "./message-list";
import { ChatInput } from "./chat-input";
import { ModeToggle } from "./mode-toggle";
import { Logo } from "@/components/common/logo";
import { ThemeToggle } from "@/components/common/theme-toggle";
import { Trash2 } from "lucide-react";
import { Button } from "@/components/ui/button";

export function ChatWindow() {
    const { messages, isLoading, mode, setMode, sendUserMessage, clearChat } =
        useChat();

    return (
        <div className="flex flex-col h-screen bg-secondary dark:bg-background">
            {/* Header */}
            <header className="flex-shrink-0 bg-background border-b border-border shadow-sm">
                <div className="w-[90%] max-w-screen-2xl mx-auto h-14 flex items-center justify-between">
                    <Logo size="sm" />
                    <div className="flex items-center gap-3">
                        <ModeToggle
                            mode={mode}
                            onModeChange={setMode}
                            disabled={isLoading}
                        />
                        <ThemeToggle />
                        {messages.length > 0 && (
                            <Button
                                variant="ghost"
                                size="icon"
                                onClick={clearChat}
                                disabled={isLoading}
                                className="text-muted-foreground hover:text-red-500 h-8 w-8"
                                title="Clear chat"
                            >
                                <Trash2 size={15} />
                            </Button>
                        )}
                    </div>
                </div>
            </header>

            {/* Messages */}
            <div className="flex-1 overflow-hidden w-[90%] max-w-screen-2xl mx-auto flex flex-col">
                <MessageList messages={messages} isLoading={isLoading} />
            </div>

            {/* Input */}
            <div className="flex-shrink-0 bg-background border-t border-border shadow-sm">
                <div className="w-[90%] max-w-screen-2xl mx-auto py-4">
                    <ChatInput onSend={sendUserMessage} isLoading={isLoading} />
                    <p className="text-center text-[11px] text-muted-foreground mt-2">
                        LegalQ may make mistakes. Always consult a qualified lawyer for
                        serious matters.
                    </p>
                </div>
            </div>
        </div>
    );
}
