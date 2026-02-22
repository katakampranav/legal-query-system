import Link from "next/link";
import { Navbar } from "@/components/common/navbar";
import { Button } from "@/components/ui/button";
import {
  Scale,
  MessageSquare,
  BookOpen,
  Lightbulb,
  CheckCircle2,
  Gavel,
  Shield,
  Target,
  ChevronRight,
  FileText,
  Search,
  Zap,
} from "lucide-react";

// ─── Hero ────────────────────────────────────────────────────────────────────
function HeroSection() {
  return (
    <section className="relative min-h-[90vh] flex items-center justify-center overflow-hidden pt-16">
      {/* Background */}
      <div className="absolute inset-0 bg-gradient-to-br from-accent/60 via-background to-secondary -z-10" />
      <div className="absolute top-20 left-1/3 w-96 h-96 bg-primary/10 rounded-full blur-3xl -z-10 animate-pulse" />
      <div className="absolute bottom-10 right-1/4 w-72 h-72 bg-primary/5 rounded-full blur-3xl -z-10" />

      <div className="w-[90%] max-w-screen-2xl mx-auto text-center">
        {/* Badge */}
        <div className="inline-flex items-center gap-2 bg-accent border border-primary/20 rounded-full px-4 py-1.5 text-sm text-primary font-medium mb-8">
          <Zap size={14} className="fill-primary text-primary" />
          Powered by AI · Based on Bharatiya Nyaya Sanhita
        </div>

        <h1 className="text-6xl sm:text-7xl md:text-[8rem] font-black tracking-tight mb-6">
          <span className="bg-gradient-to-r from-[#d97757] via-[#c4623c] to-[#a8512f] bg-clip-text text-transparent">
            LegalQ
          </span>
        </h1>

        <p className="text-xl sm:text-2xl text-foreground/70 max-w-3xl mx-auto leading-relaxed mb-4">
          Understand crimes, punishments, and your{" "}
          <span className="text-primary font-semibold">legal rights</span>{" "}
          under Indian law — explained in plain language.
        </p>
        <p className="text-foreground/50 text-base max-w-2xl mx-auto mb-10">
          No jargon. No confusion. Just clear answers grounded in the Bharatiya
          Nyaya Sanhita using AI.
        </p>

        <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
          <Link href="/chat">
            <Button size="lg" className="gap-2 shadow-lg shadow-primary/20 text-base px-8">
              <MessageSquare size={18} />
              Start Asking
              <ChevronRight size={16} />
            </Button>
          </Link>
          <a href="#how-it-works">
            <Button variant="outline" size="lg" className="gap-2 text-base px-8 border-border text-foreground">
              <BookOpen size={18} />
              How it Works
            </Button>
          </a>
        </div>

        <div className="flex items-center justify-center gap-6 mt-12 flex-wrap">
          {["Indian Criminal Law", "BNS 2023", "AI Powered", "Free to Use"].map((tag) => (
            <div key={tag} className="flex items-center gap-1.5 text-sm text-foreground/40">
              <CheckCircle2 size={14} className="text-green-500" />
              {tag}
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

// ─── How It Works ────────────────────────────────────────────────────────────
const steps = [
  {
    icon: FileText,
    step: "01",
    title: "Describe your situation",
    description: "Type your legal question or describe the incident in plain language. No legal knowledge required.",
  },
  {
    icon: Search,
    step: "02",
    title: "AI finds relevant law",
    description: "LegalQ searches the Bharatiya Nyaya Sanhita to find the most applicable sections for your situation.",
  },
  {
    icon: Lightbulb,
    step: "03",
    title: "Get a clear explanation",
    description: "Receive a simple, structured explanation of the law, punishments, and what steps you can take.",
  },
];

function HowItWorksSection() {
  return (
    <section id="how-it-works" className="py-24 bg-background">
      <div className="w-[90%] max-w-screen-2xl mx-auto">
        <div className="text-center mb-16">
          <p className="text-primary font-semibold text-sm uppercase tracking-widest mb-3">Simple Process</p>
          <h2 className="text-4xl font-bold text-foreground mb-4">How LegalQ Works</h2>
          <p className="text-muted-foreground max-w-xl mx-auto">
            Getting legal clarity takes just three steps. No sign-up, no waiting.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {steps.map((item) => {
            const Icon = item.icon;
            return (
              <div
                key={item.step}
                className="relative group bg-secondary rounded-2xl p-8 border border-border hover:border-primary/30 hover:shadow-lg hover:-translate-y-1 transition-all duration-300"
              >
                <div className="text-7xl font-black text-border group-hover:text-primary/10 absolute top-4 right-6 select-none transition-colors duration-300">
                  {item.step}
                </div>
                <div className="bg-gradient-to-br from-primary to-[#b85d38] text-white w-12 h-12 rounded-xl flex items-center justify-center mb-5 shadow-md">
                  <Icon size={22} />
                </div>
                <h3 className="text-lg font-bold text-foreground mb-2">{item.title}</h3>
                <p className="text-muted-foreground text-sm leading-relaxed">{item.description}</p>
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
}

// ─── Two Modes ───────────────────────────────────────────────────────────────
function ModesSection() {
  return (
    <section className="py-24 bg-[#1e140a] dark:bg-[#120d07]">
      <div className="w-[90%] max-w-screen-2xl mx-auto">
        <div className="text-center mb-16">
          <p className="text-primary font-semibold text-sm uppercase tracking-widest mb-3">Two Modes</p>
          <h2 className="text-4xl font-bold text-white mb-4">Choose Your Explanation Style</h2>
          <p className="text-white/50 max-w-xl mx-auto">
            Not everyone needs the same level of detail. LegalQ adapts to you.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          {/* Normal Mode */}
          <div className="bg-white/5 border border-white/10 rounded-2xl p-8 hover:bg-white/10 transition-all duration-300">
            <div className="flex items-center gap-3 mb-6">
              <div className="bg-primary/20 text-primary w-12 h-12 rounded-xl flex items-center justify-center">
                <Scale size={22} />
              </div>
              <div>
                <div className="text-xs text-primary font-semibold uppercase tracking-wide mb-0.5">Mode 1</div>
                <h3 className="text-xl font-bold text-white">Normal Mode</h3>
              </div>
            </div>
            <p className="text-white/50 text-sm mb-6">
              Perfect for everyday citizens who want to understand their rights without legal expertise.
            </p>
            <ul className="space-y-3">
              {["What the law says in plain language", "Simple explanation of the situation", "What you can do next", "Safe, grounded answers"].map((point) => (
                <li key={point} className="flex items-start gap-2 text-sm text-white/70">
                  <CheckCircle2 size={16} className="text-green-400 mt-0.5 flex-shrink-0" />
                  {point}
                </li>
              ))}
            </ul>
          </div>

          {/* Lawyer Mode */}
          <div className="bg-primary/15 border border-primary/30 rounded-2xl p-8 hover:bg-primary/25 transition-all duration-300 relative overflow-hidden">
            <div className="absolute top-4 right-4 bg-primary text-white text-[10px] font-bold px-2 py-0.5 rounded-full uppercase tracking-wide">
              Advanced
            </div>
            <div className="flex items-center gap-3 mb-6">
              <div className="bg-primary/20 text-primary w-12 h-12 rounded-xl flex items-center justify-center">
                <Gavel size={22} />
              </div>
              <div>
                <div className="text-xs text-primary font-semibold uppercase tracking-wide mb-0.5">Mode 2</div>
                <h3 className="text-xl font-bold text-white">Lawyer Mode</h3>
              </div>
            </div>
            <p className="text-white/50 text-sm mb-6">
              Structured legal analysis for legal professionals, students, or informed citizens.
            </p>
            <ul className="space-y-3">
              {["Relevant BNS sections & clauses", "Punishment and sentencing details", "Legal reasoning and precedents", "Procedural next steps"].map((point) => (
                <li key={point} className="flex items-start gap-2 text-sm text-white/70">
                  <CheckCircle2 size={16} className="text-primary mt-0.5 flex-shrink-0" />
                  {point}
                </li>
              ))}
            </ul>
          </div>
        </div>
      </div>
    </section>
  );
}

// ─── Why LegalQ ──────────────────────────────────────────────────────────────
const features = [
  {
    icon: Shield,
    title: "Based on Indian Criminal Law",
    description: "All answers are grounded exclusively in the Bharatiya Nyaya Sanhita (BNS) 2023, the current Indian criminal code.",
  },
  {
    icon: Target,
    title: "Context-grounded Answers",
    description: "LegalQ retrieves the most relevant legal provisions for your specific situation — not generic advice.",
  },
  {
    icon: Scale,
    title: "Safe Refusal Policy",
    description: "For questions outside Indian criminal law, LegalQ safely declines rather than hallucinating inaccurate answers.",
  },
];

function WhyLegalQSection() {
  return (
    <section className="py-24 bg-background">
      <div className="w-[90%] max-w-screen-2xl mx-auto">
        <div className="text-center mb-16">
          <p className="text-primary font-semibold text-sm uppercase tracking-widest mb-3">Why LegalQ</p>
          <h2 className="text-4xl font-bold text-foreground mb-4">Built for Accuracy & Trust</h2>
          <p className="text-muted-foreground max-w-xl mx-auto">
            Legal misinformation can be costly. LegalQ is designed with safety-first principles.
          </p>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {features.map((feature) => {
            const Icon = feature.icon;
            return (
              <div
                key={feature.title}
                className="text-center group p-8 rounded-2xl border border-border hover:border-primary/30 hover:shadow-lg hover:-translate-y-1 transition-all duration-300"
              >
                <div className="inline-flex items-center justify-center w-14 h-14 bg-accent group-hover:bg-primary/15 rounded-2xl mb-5 transition-colors duration-300">
                  <Icon size={26} className="text-primary" />
                </div>
                <h3 className="text-lg font-bold text-foreground mb-3">{feature.title}</h3>
                <p className="text-muted-foreground text-sm leading-relaxed">{feature.description}</p>
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
}

// ─── CTA ─────────────────────────────────────────────────────────────────────
function CTASection() {
  return (
    <section className="py-24 bg-gradient-to-br from-primary to-[#b85d38] relative overflow-hidden">
      <div className="absolute -top-20 -right-20 w-80 h-80 bg-white/5 rounded-full blur-2xl" />
      <div className="absolute -bottom-20 -left-20 w-80 h-80 bg-white/5 rounded-full blur-2xl" />
      <div className="w-[90%] max-w-screen-2xl mx-auto text-center relative">
        <div className="w-16 h-16 bg-white/15 rounded-2xl flex items-center justify-center mx-auto mb-6">
          <Scale size={32} className="text-white" />
        </div>
        <h2 className="text-4xl sm:text-5xl font-black text-white mb-5">Know Your Rights Today</h2>
        <p className="text-white/70 text-lg max-w-xl mx-auto mb-10">
          Stop wondering what the law says. Get instant, AI-powered legal clarity — for free.
        </p>
        <Link href="/chat">
          <Button
            size="lg"
            className="bg-white text-primary hover:bg-secondary gap-2 shadow-xl shadow-black/20 text-base px-10 font-bold"
          >
            <MessageSquare size={18} />
            Ask Your Legal Question
            <ChevronRight size={16} />
          </Button>
        </Link>
      </div>
    </section>
  );
}

// ─── Footer ──────────────────────────────────────────────────────────────────
function Footer() {
  return (
    <footer className="py-8 border-t border-border bg-secondary">
      <div className="w-[90%] max-w-screen-2xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-4">
        <p className="text-muted-foreground text-sm">© 2025 LegalQ. Built for informational purposes only.</p>
        <p className="text-muted-foreground text-sm">Not a substitute for qualified legal advice.</p>
      </div>
    </footer>
  );
}

// ─── Page ─────────────────────────────────────────────────────────────────────
export default function HomePage() {
  return (
    <>
      <Navbar />
      <main>
        <HeroSection />
        <HowItWorksSection />
        <ModesSection />
        <WhyLegalQSection />
        <CTASection />
      </main>
      <Footer />
    </>
  );
}
