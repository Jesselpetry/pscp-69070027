"use client";

import Link from "next/link";
import { useLocale } from "@/lib/i18n";

export function Navbar() {
  const { locale, setLocale } = useLocale();
  return (
    <nav className="sticky top-0 z-10 h-16 bg-card border-b shadow-[0_1px_2px_0_rgba(0,0,0,0.05)] px-6 flex items-center justify-between">
      <div className="flex items-center gap-8">
        <Link href="/" className="font-mono text-xl font-bold flex items-center">
          <span className="text-primary">&lt;i</span>help
          <span className="text-primary">&gt;</span>
        </Link>
        <span className="hidden sm:block text-sm text-muted-foreground">
          PSCP Learning-Log Maker · IT KMITL
        </span>
      </div>
      <div className="flex items-center gap-3">
        <div className="flex rounded-full border overflow-hidden text-xs font-semibold">
          {(["th", "en"] as const).map((l) => (
            <button
              key={l}
              onClick={() => setLocale(l)}
              className={
                "px-3 py-1.5 transition-colors " +
                (locale === l
                  ? "bg-primary text-primary-foreground"
                  : "bg-card text-muted-foreground hover:text-foreground")
              }
            >
              {l.toUpperCase()}
            </button>
          ))}
        </div>
        <a
          href="https://ijudge.it.kmitl.ac.th"
          target="_blank"
          rel="noreferrer"
          className="text-sm text-muted-foreground hover:text-primary"
        >
          iJudge ↗
        </a>
      </div>
    </nav>
  );
}
