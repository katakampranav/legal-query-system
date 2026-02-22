"use client";

import { Scale, Gavel } from "lucide-react";
import { cn } from "@/lib/utils";
import type { ChatMode } from "../types/chat-types";

interface ModeToggleProps {
    mode: ChatMode;
    onModeChange: (mode: ChatMode) => void;
    disabled?: boolean;
}

export function ModeToggle({ mode, onModeChange, disabled }: ModeToggleProps) {
    return (
        <div className="flex items-center gap-0.5 bg-muted border border-border p-0.5 rounded-xl">
            <button
                onClick={() => onModeChange("normal")}
                disabled={disabled}
                className={cn(
                    "flex items-center gap-2 px-4 py-1.5 rounded-lg text-sm font-semibold transition-all duration-200",
                    mode === "normal"
                        ? "bg-background text-primary shadow-sm"
                        : "text-muted-foreground hover:text-foreground"
                )}
            >
                <Scale size={15} />
                Normal
            </button>
            <button
                onClick={() => onModeChange("lawyer")}
                disabled={disabled}
                className={cn(
                    "flex items-center gap-2 px-4 py-1.5 rounded-lg text-sm font-semibold transition-all duration-200",
                    mode === "lawyer"
                        ? "bg-background text-primary shadow-sm"
                        : "text-muted-foreground hover:text-foreground"
                )}
            >
                <Gavel size={15} />
                Lawyer
            </button>
        </div>
    );
}
