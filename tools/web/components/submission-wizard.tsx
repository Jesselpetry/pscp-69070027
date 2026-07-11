"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Checkbox } from "@/components/ui/checkbox";
import { FileLanguagePicker, WizardFrame } from "@/components/wizard/wizard-frame";
import { ChoiceBadges, TextField } from "@/components/form-fields";

const STATUS_COLORS = { Pass: "green", "Not Pass": "red", "Not Submit": "gray" } as const;
const RESULT_COLORS = { Pass: "green", "Not Pass": "red" } as const;
const FACT_COLORS = { Yes: "amber", No: "gray" } as const;
const COPIED_COLORS = { No: "green", Yes: "red" } as const;
import { SUBMISSION_CERT_STATEMENTS, statementLabel } from "@/lib/statements";
import { SUBMISSION_STEPS, TIME_OPTIONS, HOW_TO_COUNT_TIME } from "@/lib/wizard-content";
import { useDraft, downloadMarkdown } from "@/lib/draft";
import { useLocale, t } from "@/lib/i18n";

const STEP_KEYS = [
  "language", "info", "understanding", "first_plan", "final_approach",
  "tests", "ai_use", "human_help", "declaration", "download",
] as const;

interface Draft {
  file_locale: "th" | "en";
  oj_title: string;
  submission_id: string;
  oj_status: string;
  time_spent: string;
  understanding: string;
  first_plan: string;
  final_approach: string;
  tests: { why: string; input: string; expected: string; actual: string; result: string }[];
  used_ai: string;
  human_help: string;
  who_helped: string;
  what_help: string;
  still_own_work: string;
  copied_code: string;
  certs: boolean[];
}

function emptyDraft(ojTitle: string): Draft {
  return {
    file_locale: "th",
    oj_title: ojTitle,
    submission_id: "",
    oj_status: "Pass",
    time_spent: "15-30 minutes",
    understanding: "",
    first_plan: "",
    final_approach: "",
    tests: [0, 1, 2].map(() => ({ why: "", input: "", expected: "", actual: "", result: "Pass" })),
    used_ai: "No",
    human_help: "No",
    who_helped: "",
    what_help: "",
    still_own_work: "",
    copied_code: "No",
    certs: SUBMISSION_CERT_STATEMENTS.map(() => false),
  };
}

const L = {
  ojTitle: { th: "หมายเลข/ชื่อโจทย์ OJ", en: "OJ problem number/title" },
  subId: { th: "OJ submission ID (ถ้ามี)", en: "OJ submission ID, if submitted" },
  status: { th: "สถานะ OJ", en: "OJ status" },
  time: { th: "เวลาที่ใช้คิดและทำโจทย์ด้วยตนเอง", en: "Independent time spent" },
  understanding: {
    th: "อธิบายโจทย์ด้วยคำพูดของตนเอง (input / output / constraints)",
    en: "The problem in your own words (input / output / constraints)",
  },
  firstPlan: { th: "แผนแรกของฉัน", en: "My first plan" },
  finalApproach: { th: "วิธีสุดท้ายที่ใช้จริง", en: "My final approach" },
  testWhy: { th: "ทำไมเลือก case นี้", en: "Why I chose this case" },
  input: { th: "Input", en: "Input" },
  expected: { th: "Expected output", en: "Expected output" },
  actual: { th: "Actual output", en: "Actual output" },
  result: { th: "Result", en: "Result" },
  usedAi: { th: "ใช้ AI กับโจทย์นี้หรือไม่", en: "Did you use AI for this problem?" },
  aiYesNote: {
    th: "คุณตอบว่าใช้ AI — อย่าลืมสร้าง ai_reflection.md ด้วย (ปุ่มอยู่หน้ารายการโจทย์)",
    en: "You answered Yes — remember to also create ai_reflection.md (button on the problems page).",
  },
  humanHelp: {
    th: "ได้ถามเพื่อน TA ผู้สอน หรือบุคคลอื่นหรือไม่",
    en: "Did you ask a friend, TA, instructor, or another person for help?",
  },
  whoHelped: { th: "ใครช่วยคุณ", en: "Who helped you?" },
  whatHelp: { th: "เขาช่วยอะไร", en: "What did they help with?" },
  stillOwn: { th: "คุณยังทำอะไรด้วยตนเอง", en: "What did you still do by yourself?" },
  copied: { th: "คุณคัดลอก code จากคนอื่นหรือไม่", en: "Did you copy any code from another person?" },
  certWarn: {
    th: "ติ๊กเฉพาะข้อที่เป็นจริงเท่านั้น ข้อที่ไม่ติ๊กจะถูกเว้นว่างในไฟล์",
    en: "Check only true statements. Unchecked statements stay blank in the file.",
  },
  preview: { th: "สร้างตัวอย่างไฟล์", en: "Generate preview" },
  download: { th: "ดาวน์โหลด submission.md", en: "Download submission.md" },
  clear: { th: "ล้างแบบร่างนี้", en: "Clear this draft" },
  draftNote: {
    th: "แบบร่างถูกบันทึกในเครื่องของคุณโดยอัตโนมัติ",
    en: "Your draft is saved automatically in this browser.",
  },
  vscodeReminder: {
    th: "อย่าลืม: เขียน รัน และทดสอบ code จริงใน VS Code และส่ง code ในระบบ OJ ด้วยตนเอง",
    en: "Remember: write, run, and test your real code in VS Code, and submit the code to the OJ yourself.",
  },
};

export function SubmissionWizard({ problemId, ojTitle }: { problemId: string; ojTitle: string }) {
  const { locale } = useLocale();
  const [draft, setDraft, clearDraft] = useDraft<Draft>(
    `ihelp-submission-${problemId}`,
    emptyDraft(ojTitle),
  );
  const [stepIndex, setStepIndex] = useState(0);
  const [preview, setPreview] = useState("");
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);

  const steps = STEP_KEYS.map((k) => SUBMISSION_STEPS[k]);
  const key = STEP_KEYS[stepIndex];
  const patch = (p: Partial<Draft>) => setDraft((d) => ({ ...d, ...p }));
  const patchTest = (i: number, p: Partial<Draft["tests"][number]>) =>
    setDraft((d) => ({
      ...d,
      tests: d.tests.map((tc, j) => (j === i ? { ...tc, ...p } : tc)),
    }));

  async function generate(): Promise<string> {
    const certifications: Record<string, boolean> = {};
    SUBMISSION_CERT_STATEMENTS.forEach((s, i) => (certifications[s] = draft.certs[i]));
    const askedHuman = draft.human_help === "Yes";
    const fields: Record<string, unknown> = {
      oj_title: draft.oj_title,
      submission_id: draft.submission_id,
      oj_status: draft.oj_status,
      time_spent: draft.time_spent,
      understanding: draft.understanding,
      first_plan: draft.first_plan,
      final_approach: draft.final_approach,
      used_ai: draft.used_ai,
      human_help: draft.human_help,
      // hidden fields stay out of the file when no human help was used
      who_helped: askedHuman ? draft.who_helped : "",
      what_help: askedHuman ? draft.what_help : "",
      still_own_work: askedHuman ? draft.still_own_work : "",
      copied_code: draft.copied_code,
      certifications,
    };
    draft.tests.forEach((tc, i) => {
      const n = i + 1;
      fields[`t${n}_why`] = tc.why;
      fields[`t${n}_input`] = tc.input;
      fields[`t${n}_expected`] = tc.expected;
      fields[`t${n}_actual`] = tc.actual;
      fields[`t${n}_result`] = tc.result;
    });
    const res = await fetch("/api/generate/submission", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ locale: draft.file_locale, fields }),
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.error || "generation failed");
    return data.markdown;
  }

  async function refreshPreview() {
    setBusy(true);
    setError("");
    try {
      setPreview(await generate());
    } catch (e) {
      setError((e as Error).message);
    } finally {
      setBusy(false);
    }
  }

  async function download() {
    setBusy(true);
    setError("");
    try {
      downloadMarkdown("submission.md", await generate());
    } catch (e) {
      setError((e as Error).message);
    } finally {
      setBusy(false);
    }
  }

  return (
    <WizardFrame
      fileName="submission.md"
      problemLabel={ojTitle}
      steps={steps}
      stepIndex={stepIndex}
      onStepChange={(i) => {
        setStepIndex(i);
        if (STEP_KEYS[i] === "download") setPreview("");
      }}
    >
      {key === "language" && (
        <FileLanguagePicker
          value={draft.file_locale}
          onChange={(v) => patch({ file_locale: v })}
        />
      )}

      {key === "info" && (
        <div className="space-y-4">
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <TextField label={t(L.ojTitle, locale)} value={draft.oj_title} onChange={(v) => patch({ oj_title: v })} rows={2} />
            <TextField label={t(L.subId, locale)} value={draft.submission_id} onChange={(v) => patch({ submission_id: v })} rows={2} />
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <ChoiceBadges label={t(L.status, locale)} value={draft.oj_status} onChange={(v) => patch({ oj_status: v })} options={["Pass", "Not Pass", "Not Submit"]} colors={STATUS_COLORS} />
            <ChoiceBadges label={t(L.time, locale)} value={draft.time_spent} onChange={(v) => patch({ time_spent: v })} options={TIME_OPTIONS} />
          </div>
          <p className="text-xs text-muted-foreground whitespace-pre-line rounded-lg border bg-background/50 p-3">
            {t(HOW_TO_COUNT_TIME, locale)}
          </p>
        </div>
      )}

      {key === "understanding" && (
        <TextField label={t(L.understanding, locale)} value={draft.understanding} onChange={(v) => patch({ understanding: v })} rows={8} />
      )}

      {key === "first_plan" && (
        <TextField label={t(L.firstPlan, locale)} value={draft.first_plan} onChange={(v) => patch({ first_plan: v })} rows={8} />
      )}

      {key === "final_approach" && (
        <TextField label={t(L.finalApproach, locale)} value={draft.final_approach} onChange={(v) => patch({ final_approach: v })} rows={8} />
      )}

      {key === "tests" && (
        <div className="space-y-4">
          {draft.tests.map((tc, i) => (
            <div key={i} className="rounded-lg border bg-background/50 p-4 space-y-3">
              <div className="grid grid-cols-1 sm:grid-cols-[2fr_1fr] gap-4">
                <TextField label={`Test ${i + 1} — ${t(L.testWhy, locale)}`} value={tc.why} onChange={(v) => patchTest(i, { why: v })} rows={2} />
                <ChoiceBadges label={t(L.result, locale)} value={tc.result} onChange={(v) => patchTest(i, { result: v })} options={["Pass", "Not Pass"]} colors={RESULT_COLORS} />
              </div>
              <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
                <TextField label={t(L.input, locale)} value={tc.input} onChange={(v) => patchTest(i, { input: v })} rows={3} />
                <TextField label={t(L.expected, locale)} value={tc.expected} onChange={(v) => patchTest(i, { expected: v })} rows={3} />
                <TextField label={t(L.actual, locale)} value={tc.actual} onChange={(v) => patchTest(i, { actual: v })} rows={3} />
              </div>
            </div>
          ))}
        </div>
      )}

      {key === "ai_use" && (
        <div className="space-y-3">
          <ChoiceBadges label={t(L.usedAi, locale)} value={draft.used_ai} onChange={(v) => patch({ used_ai: v })} options={["No", "Yes"]} colors={FACT_COLORS} />
          {draft.used_ai === "Yes" && (
            <p className="text-sm text-primary rounded-lg border border-primary/40 bg-primary/5 p-3">
              {t(L.aiYesNote, locale)}
            </p>
          )}
        </div>
      )}

      {key === "human_help" && (
        <div className="space-y-4">
          <ChoiceBadges label={t(L.humanHelp, locale)} value={draft.human_help} onChange={(v) => patch({ human_help: v })} options={["No", "Yes"]} colors={FACT_COLORS} />
          {draft.human_help === "Yes" && (
            <>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <TextField label={t(L.whoHelped, locale)} value={draft.who_helped} onChange={(v) => patch({ who_helped: v })} rows={2} />
                <TextField label={t(L.whatHelp, locale)} value={draft.what_help} onChange={(v) => patch({ what_help: v })} rows={2} />
              </div>
              <TextField label={t(L.stillOwn, locale)} value={draft.still_own_work} onChange={(v) => patch({ still_own_work: v })} rows={3} />
            </>
          )}
          <ChoiceBadges label={t(L.copied, locale)} value={draft.copied_code} onChange={(v) => patch({ copied_code: v })} options={["No", "Yes"]} colors={COPIED_COLORS} />
        </div>
      )}

      {key === "declaration" && (
        <div className="space-y-2">
          <p className="text-xs text-muted-foreground">{t(L.certWarn, locale)}</p>
          {SUBMISSION_CERT_STATEMENTS.map((s, i) => (
            <label key={s} className="flex items-center gap-3 text-sm cursor-pointer rounded-lg border bg-background px-3 py-2.5 hover:bg-muted transition-colors">
              <Checkbox
                checked={draft.certs[i]}
                onCheckedChange={(v) =>
                  setDraft((d) => ({ ...d, certs: d.certs.map((x, j) => (j === i ? v === true : x)) }))
                }
              />
              <span>
                {statementLabel(s, locale)}
                {locale === "th" && (
                  <span className="block text-xs text-muted-foreground/80">{s}</span>
                )}
              </span>
            </label>
          ))}
        </div>
      )}

      {key === "download" && (
        <div className="space-y-4">
          <div className="flex flex-wrap gap-2">
            <Button variant="outline" onClick={refreshPreview} disabled={busy}>
              {t(L.preview, locale)}
            </Button>
            <Button onClick={download} disabled={busy}>
              ⬇ {t(L.download, locale)}
            </Button>
            <Button
              variant="ghost"
              className="text-muted-foreground"
              onClick={() => {
                if (window.confirm(t(L.clear, locale) + "?")) clearDraft();
              }}
            >
              {t(L.clear, locale)}
            </Button>
          </div>
          {error && <p className="text-sm text-destructive">{error}</p>}
          <p className="text-xs text-muted-foreground">{t(L.draftNote, locale)}</p>
          <p className="text-sm rounded-lg border border-amber-300 bg-amber-50 dark:bg-amber-950 dark:border-amber-800 p-3">
            {t(L.vscodeReminder, locale)}
          </p>
          {preview && (
            <pre className="text-xs bg-background rounded-lg border p-4 whitespace-pre-wrap max-h-[50vh] overflow-y-auto">
              {preview}
            </pre>
          )}
        </div>
      )}
    </WizardFrame>
  );
}
