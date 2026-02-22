"use client";

import { useTheme } from "next-themes";
import { useEffect, useRef, useState } from "react";
import { Sun, Moon, Monitor, ChevronDown } from "lucide-react";
import { cn } from "@/lib/utils";

const themes = [
    { value: "light", icon: Sun, label: "Light" },
    { value: "dark", icon: Moon, label: "Dark" },
    { value: "system", icon: Monitor, label: "System" },
] as const;

export function ThemeToggle() {
    const { theme, setTheme, resolvedTheme } = useTheme();
    const [mounted, setMounted] = useState(false);
    const [open, setOpen] = useState(false);
    const ref = useRef<HTMLDivElement>(null);

    useEffect(() => setMounted(true), []);

    // Close on outside click
    useEffect(() => {
        function handleClick(e: MouseEvent) {
            if (ref.current && !ref.current.contains(e.target as Node)) {
                setOpen(false);
            }
        }
        if (open) document.addEventListener("mousedown", handleClick);
        return () => document.removeEventListener("mousedown", handleClick);
    }, [open]);

    if (!mounted) return <div className="w-9 h-9" />;

    const current = themes.find((t) => t.value === theme) ?? themes[2];
    const CurrentIcon = resolvedTheme === "dark" ? Moon : Sun;

    return (
        <div ref={ref} className="relative">
            {/* Trigger button — shows current resolved theme icon */}
            <button
                onClick={() => setOpen((o) => !o)}
                className={cn(
                    "flex items-center gap-1.5 h-9 px-3 rounded-lg border border-border bg-background text-muted-foreground hover:text-foreground hover:bg-muted transition-all duration-200 text-sm font-medium",
                    open && "bg-muted text-foreground"
                )}
                aria-label="Change theme"
            >
                <CurrentIcon size={15} />
                <span className="hidden sm:inline">{current.label}</span>
                <ChevronDown
                    size={13}
                    className={cn("transition-transform duration-200", open && "rotate-180")}
                />
            </button>

            {/* Dropdown */}
            {open && (
                <div className="absolute right-0 mt-2 w-40 bg-background border border-border rounded-xl shadow-lg overflow-hidden z-50 animate-in fade-in slide-in-from-top-1 duration-150">
                    {themes.map(({ value, icon: Icon, label }) => (
                        <button
                            key={value}
                            onClick={() => {
                                setTheme(value);
                                setOpen(false);
                            }}
                            className={cn(
                                "flex items-center gap-3 w-full px-4 py-2.5 text-sm transition-colors duration-150",
                                theme === value
                                    ? "text-primary bg-accent font-semibold"
                                    : "text-foreground hover:bg-muted"
                            )}
                        >
                            <Icon size={15} />
                            {label}
                            {theme === value && (
                                <span className="ml-auto w-1.5 h-1.5 rounded-full bg-primary" />
                            )}
                        </button>
                    ))}
                </div>
            )}
        </div>
    );
}
