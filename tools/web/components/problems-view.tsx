"use client";

import Link from "next/link";
import { useMemo, useState } from "react";
import type { MasterProblem } from "@/lib/master";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { WeekBadge } from "@/components/week-badge";
import { useLocale, t, type LText } from "@/lib/i18n";

const L: Record<string, LText> = {
  breadcrumb: {
    th: "Courses / [2026] Problem Solving and Computer Programming (IT)",
    en: "Courses / [2026] Problem Solving and Computer Programming (IT)",
  },
  heading: { th: "Problems", en: "Problems" },
  intro: {
    th: "เลือกโจทย์เพื่อสร้าง submission.md / ai_reflection.md แบบทีละขั้นตอน แล้วดาวน์โหลดไฟล์ไปเก็บในเครื่องของคุณ",
    en: "Pick a problem to build submission.md / ai_reflection.md step by step, then download the file to your machine.",
  },
  total: { th: "โจทย์ทั้งหมด", en: "Total problems" },
  logs: { th: "Learning logs", en: "Learning logs" },
  listTitle: { th: "รายการโจทย์ (Problems List)", en: "Problems List" },
  search: { th: "ค้นหาชื่อหรือ ID...", en: "Search name or ID..." },
  problem: { th: "ชื่อโจทย์", en: "Problem" },
  difficulty: { th: "ความยาก", en: "Difficulty" },
  actions: { th: "สร้างไฟล์ (Learning Log)", en: "Make files (Learning Log)" },
  expires: { th: "หมดเขต", en: "Expires" },
  expired: { th: "หมดเขตแล้ว", en: "Expired" },
  learningLog: { th: "Learning Log", en: "Learning Log" },
  submissionBtn: { th: "สร้าง submission.md", en: "Make submission.md" },
  reflectionBtn: { th: "สร้าง ai_reflection.md", en: "Make ai_reflection.md" },
  openProblem: { th: "เปิดโจทย์บน iJudge", en: "Open on iJudge" },
  llOnly: {
    th: "submission.md ต้องทำเฉพาะโจทย์ที่มีป้าย Learning Log (แสดงไว้ด้านบนสุด) ส่วน ai_reflection.md สร้างได้กับทุกโจทย์ที่ใช้ AI",
    en: "submission.md is required only for problems tagged Learning Log (sorted to the top). ai_reflection.md can be made for any problem where AI was used.",
  },
  empty: { th: "ไม่พบโจทย์ที่ตรงกับตัวกรอง", en: "No problems match the filter." },
  all: { th: "All", en: "All" },
};

function DifficultyStars({ value }: { value: number }) {
  if (value <= 0) {
    return <span className="text-sm text-muted-foreground/50">—</span>;
  }
  return (
    <span className="whitespace-nowrap text-base" title={`difficulty ${value}`}>
      <span className="text-amber-400">{"★".repeat(value)}</span>
      <span className="text-border">{"★".repeat(5 - value)}</span>
    </span>
  );
}

export function ProblemsView({ problems }: { problems: MasterProblem[] }) {
  const { locale } = useLocale();
  const [query, setQuery] = useState("");
  const [weekFilter, setWeekFilter] = useState<number | "all">("all");

  const weeks = useMemo(
    () =>
      [...new Set(problems.map((p) => p.week).filter((w): w is number => w !== null))].sort(
        (a, b) => a - b,
      ),
    [problems],
  );

  const filtered = useMemo(() => {
    const q = query.trim().toLowerCase();
    return problems
      .filter((p) => {
        if (weekFilter !== "all" && p.week !== weekFilter) return false;
        if (!q) return true;
        return p.name.toLowerCase().includes(q) || String(p.id).includes(q);
      })
      // learning-log problems first: they are the ones that require submission.md
      .sort((a, b) =>
        a.learningLog !== b.learningLog ? (a.learningLog ? -1 : 1) : a.id - b.id,
      );
  }, [problems, query, weekFilter]);

  return (
    <main className="max-w-6xl mx-auto px-6 py-8 w-full">
      <div className="mb-6">
        <p className="text-sm text-muted-foreground mb-1">{t(L.breadcrumb, locale)}</p>
        <h1 className="text-4xl font-bold">{t(L.heading, locale)}</h1>
        <p className="text-sm text-muted-foreground mt-2">{t(L.intro, locale)}</p>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-2 gap-4 mb-6">
        {[
          { label: t(L.total, locale), value: problems.length },
          { label: t(L.logs, locale), value: problems.filter((p) => p.learningLog).length },
        ].map((s) => (
          <div key={s.label} className="bg-card rounded-2xl border shadow-sm px-5 py-4">
            <p className="text-xs text-muted-foreground font-medium uppercase tracking-wide">
              {s.label}
            </p>
            <p className="text-2xl font-bold mt-1">{s.value}</p>
          </div>
        ))}
      </div>

      <div className="bg-card rounded-2xl border shadow-sm overflow-hidden">
        <div className="flex flex-wrap items-center gap-3 px-6 py-5 border-b">
          <h3 className="text-xl font-semibold mr-auto">{t(L.listTitle, locale)}</h3>
          <Input
            placeholder={t(L.search, locale)}
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            className="w-52"
          />
        </div>

        {weeks.length > 0 && (
          <div className="flex flex-wrap items-center gap-2 px-6 py-3 border-b bg-background/50">
            <span className="text-xs font-medium text-muted-foreground uppercase tracking-wide mr-1">
              Week
            </span>
            <Button
              size="sm"
              variant={weekFilter === "all" ? "default" : "outline"}
              className="h-7 rounded-full px-3 text-xs"
              onClick={() => setWeekFilter("all")}
            >
              {t(L.all, locale)}
            </Button>
            {weeks.map((w) => (
              <Button
                key={w}
                size="sm"
                variant={weekFilter === w ? "default" : "outline"}
                className="h-7 rounded-full px-3 text-xs"
                onClick={() => setWeekFilter(w)}
              >
                Week {w}
              </Button>
            ))}
          </div>
        )}

        <div className="overflow-x-auto">
          <Table>
            <TableHeader>
              <TableRow className="bg-background hover:bg-background">
                <TableHead>{t(L.problem, locale)}</TableHead>
                <TableHead>{t(L.difficulty, locale)}</TableHead>
                <TableHead>{t(L.actions, locale)}</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {filtered.length === 0 ? (
                <TableRow>
                  <TableCell colSpan={3} className="py-16 text-center text-muted-foreground">
                    {t(L.empty, locale)}
                  </TableCell>
                </TableRow>
              ) : (
                filtered.map((p) => {
                  const expired = p.expireIso !== null && new Date(p.expireIso) < new Date();
                  return (
                    <TableRow key={p.id} className="hover:bg-background/60">
                      <TableCell className="py-4">
                        <div className="flex items-center gap-2.5">
                          <a
                            href={p.url}
                            target="_blank"
                            rel="noreferrer"
                            title={t(L.openProblem, locale)}
                            className="text-primary font-semibold text-base hover:underline"
                          >
                            {p.name}
                          </a>
                          {p.learningLog && (
                            <Badge
                              variant="outline"
                              className="border-primary/30 bg-primary/10 text-primary font-medium"
                            >
                              {t(L.learningLog, locale)}
                            </Badge>
                          )}
                        </div>
                        <div className="flex flex-wrap items-center gap-x-2.5 gap-y-1 mt-1.5 text-xs text-muted-foreground">
                          <span className="font-mono">#{p.id}</span>
                          {p.week !== null && (
                            <>
                              <span className="text-border">·</span>
                              <WeekBadge week={p.week} />
                            </>
                          )}
                          <span className="text-border">·</span>
                          <span className={expired ? "text-destructive font-medium" : ""}>
                            {t(expired ? L.expired : L.expires, locale)} {p.expireLabel}
                          </span>
                        </div>
                      </TableCell>
                      <TableCell className="py-4">
                        <DifficultyStars value={p.difficulty} />
                      </TableCell>
                      <TableCell className="py-4">
                        <div className="flex flex-wrap gap-2">
                          {p.learningLog && (
                            <Button
                              asChild
                              size="sm"
                              className="h-8 text-xs font-medium"
                            >
                              <Link href={`/make/submission?problem=${p.id}`}>
                                {t(L.submissionBtn, locale)}
                              </Link>
                            </Button>
                          )}
                          <Button
                            asChild
                            size="sm"
                            variant="outline"
                            className="h-8 text-xs font-medium text-muted-foreground hover:text-foreground"
                          >
                            <Link href={`/make/reflection?problem=${p.id}`}>
                              {t(L.reflectionBtn, locale)}
                            </Link>
                          </Button>
                        </div>
                      </TableCell>
                    </TableRow>
                  );
                })
              )}
            </TableBody>
          </Table>
        </div>
        <p className="px-6 py-3 border-t text-xs text-muted-foreground">{t(L.llOnly, locale)}</p>
      </div>
    </main>
  );
}
