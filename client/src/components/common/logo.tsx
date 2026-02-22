import Link from "next/link";
import { Scale } from "lucide-react";

interface LogoProps {
    size?: "sm" | "md" | "lg";
}

const sizeMap = {
    sm: { icon: 18, text: "text-lg" },
    md: { icon: 22, text: "text-xl" },
    lg: { icon: 28, text: "text-3xl" },
};

export function Logo({ size = "md" }: LogoProps) {
    const { icon, text } = sizeMap[size];

    return (
        <Link href="/" className="flex items-center gap-2 group">
            <div className="relative">
                <div className="absolute inset-0 bg-primary/30 rounded-full blur-md group-hover:blur-lg transition-all duration-300" />
                <div className="relative bg-gradient-to-br from-primary to-[#b85d38] text-white p-2 rounded-xl shadow-lg">
                    <Scale size={icon} strokeWidth={2.5} />
                </div>
            </div>
            <span
                className={`${text} font-extrabold tracking-tight bg-gradient-to-r from-primary to-[#b85d38] bg-clip-text text-transparent`}
            >
                LegalQ
            </span>
        </Link>
    );
}
