import fs from "fs";
import { OJ_PROBLEMS_FILE } from "./paths";

// Shape of one entry in oj_problems.json (exported from iJudge).
interface RawProblem {
  id: number;
  name: string;
  status: string; // "Passed" | "Not Passed"
  difficulty: number;
  passed_count: number;
  attempt_count: number;
  percentage: number;
  expire_date: string; // e.g. "31 July 2026, 00:00"
  is_learning_log: boolean;
  url: string;
}

export interface MasterProblem {
  id: number;
  name: string;
  difficulty: number;
  expireIso: string | null; // "YYYY-MM-DDTHH:mm"
  expireLabel: string;
  week: number | null;
  learningLog: boolean;
  url: string;
}

const MONTHS: Record<string, string> = {
  january: "01", february: "02", march: "03", april: "04",
  may: "05", june: "06", july: "07", august: "08",
  september: "09", october: "10", november: "11", december: "12",
};

// "31 July 2026, 00:00" -> "2026-07-31T00:00"
export function parseExpire(expire: string): string | null {
  const m = expire.trim().match(/^(\d{1,2})\s+([A-Za-z]+)\s+(\d{4}),?\s*(\d{2}):(\d{2})$/);
  if (!m) return null;
  const month = MONTHS[m[2].toLowerCase()];
  if (!month) return null;
  return `${m[3]}-${month}-${m[1].padStart(2, "0")}T${m[4]}:${m[5]}`;
}

export function loadProblems(): MasterProblem[] {
  const raw: RawProblem[] = JSON.parse(fs.readFileSync(OJ_PROBLEMS_FILE, "utf-8"));

  // Week number derived from distinct expire dates, sorted ascending:
  // earliest = Week 1, next distinct date = Week 2, ...
  const dates = [...new Set(
    raw.map((p) => parseExpire(p.expire_date)).filter((d): d is string => d !== null),
  )].sort();
  const weekOf = new Map(dates.map((d, i) => [d, i + 1]));

  const problems = raw.map((p): MasterProblem => {
    const iso = parseExpire(p.expire_date);
    return {
      id: p.id,
      name: p.name,
      difficulty: p.difficulty,
      expireIso: iso,
      expireLabel: p.expire_date,
      week: iso ? weekOf.get(iso)! : null,
      learningLog: p.is_learning_log,
      url: p.url,
    };
  });
  problems.sort((a, b) => a.id - b.id);
  return problems;
}
