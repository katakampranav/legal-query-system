"use client";

import Link from "next/link";
import { Logo } from "./logo";
import { ThemeToggle } from "./theme-toggle";
import { Button } from "@/components/ui/button";
import { MessageSquare } from "lucide-react";

export function Navbar() {
    return (
        <nav className="fixed top-0 left-0 right-0 z-50 bg-background/80 backdrop-blur-md border-b border-border shadow-sm">
            <div className="w-[90%] max-w-screen-2xl mx-auto">
                <div className="flex items-center justify-between h-16">
                    <Logo size="md" />
                    <div className="flex items-center gap-3">
                        <ThemeToggle />
                        <Link href="/chat">
                            <Button size="sm" className="gap-2 shadow-md">
                                <MessageSquare size={16} />
                                Ask a Question
                            </Button>
                        </Link>
                    </div>
                </div>
            </div>
        </nav>
    );
}
