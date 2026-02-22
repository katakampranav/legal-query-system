import { ChatWindow } from "@/features/chat/components/chat-window";
import type { Metadata } from "next";

export const metadata: Metadata = {
    title: "Chat — LegalQ",
    description: "Ask your legal questions and get AI-powered answers based on Indian criminal law.",
};

export default function ChatPage() {
    return <ChatWindow />;
}
