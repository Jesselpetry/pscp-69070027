import path from "path";

// tools/web -> repo root is two levels up
export const ROOT = path.resolve(process.cwd(), "..", "..");

// Master problem list exported from iJudge. Override with OJ_PROBLEMS_PATH.
export const OJ_PROBLEMS_FILE =
  process.env.OJ_PROBLEMS_PATH ?? path.join(ROOT, "oj_problems.json");

const TEMPLATES_DIR = path.join(ROOT, "AI-Guidelines-PSCP", "templates");

export function submissionTemplatePath(locale: "en" | "th"): string {
  return path.join(
    TEMPLATES_DIR,
    locale === "th" ? "SUBMISSION_TEMPLATE.th.md" : "SUBMISSION_TEMPLATE.md",
  );
}

export function reflectionTemplatePath(locale: "en" | "th"): string {
  return path.join(
    TEMPLATES_DIR,
    locale === "th" ? "AI_REFLECTION_TEMPLATE.th.md" : "AI_REFLECTION_TEMPLATE.md",
  );
}
