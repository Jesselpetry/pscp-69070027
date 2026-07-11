"use client";

import Link from "next/link";
import { useState } from "react";
import { Button } from "@/components/ui/button";
import { useLocale, t, type LText } from "@/lib/i18n";
import type { StepContent } from "@/lib/wizard-content";

const LABELS: Record<string, LText> = {
  back: { th: "ย้อนกลับ", en: "Back" },
  next: { th: "ถัดไป", en: "Next" },
  backToList: { th: "กลับหน้ารายการโจทย์", en: "Back to problems" },
  step: { th: "ขั้นตอนที่", en: "Step" },
  of: { th: "จาก", en: "of" },
  example: { th: "ดูตัวอย่างระดับรายละเอียดที่คาดหวัง", en: "Show an example of the expected detail" },
  exampleNote: {
    th: "ตัวอย่างจากไฟล์ examples ของรายวิชา — ห้ามคัดลอก ใช้ดูระดับรายละเอียดเท่านั้น",
    en: "Excerpt from the course example files — do not copy it; use it only to see the expected level of detail.",
  },
};

export function ExampleBox({ example }: { example: LText }) {
  const { locale } = useLocale();
  const [open, setOpen] = useState(false);
  return (
    <div className="rounded-lg border border-dashed">
      <button
        type="button"
        className="w-full text-left px-3 py-2 text-sm text-primary font-medium"
        onClick={() => setOpen((o) => !o)}
      >
        {open ? "▾" : "▸"} {t(LABELS.example, locale)}
      </button>
      {open && (
        <div className="px-3 pb-3 space-y-2">
          <p className="text-xs text-muted-foreground">{t(LABELS.exampleNote, locale)}</p>
          <pre className="text-sm bg-background rounded-md p-3 whitespace-pre-wrap font-sans border">
            {t(example, locale)}
          </pre>
        </div>
      )}
    </div>
  );
}

const FILE_LANGS: { value: "th" | "en"; label: string; sub: LText }[] = [
  {
    value: "th",
    label: "ภาษาไทย",
    sub: { th: "ใช้ template ทางการภาษาไทย", en: "Use the official Thai template" },
  },
  {
    value: "en",
    label: "English",
    sub: { th: "ใช้ template ทางการภาษาอังกฤษ", en: "Use the official English template" },
  },
];

export function FileLanguagePicker({
  value,
  onChange,
}: {
  value: "th" | "en";
  onChange: (v: "th" | "en") => void;
}) {
  const { locale } = useLocale();
  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
      {FILE_LANGS.map((lang) => (
        <button
          key={lang.value}
          type="button"
          onClick={() => onChange(lang.value)}
          className={
            "rounded-xl border-2 p-5 text-left transition-colors " +
            (value === lang.value
              ? "border-primary bg-primary/5"
              : "border-border hover:border-primary/40")
          }
        >
          <span className="flex items-center gap-2 text-lg font-bold">
            <span
              className={
                "inline-block w-3.5 h-3.5 rounded-full border-2 " +
                (value === lang.value ? "border-primary bg-primary" : "border-border")
              }
            />
            {lang.label}
          </span>
          <span className="block text-sm text-muted-foreground mt-1">
            {t(lang.sub, locale)}
          </span>
        </button>
      ))}
    </div>
  );
}

export function WizardFrame({
  fileName,
  problemLabel,
  steps,
  stepIndex,
  onStepChange,
  children,
}: {
  fileName: string;
  problemLabel: string;
  steps: StepContent[];
  stepIndex: number;
  onStepChange: (i: number) => void;
  children: React.ReactNode;
}) {
  const { locale } = useLocale();
  const step = steps[stepIndex];
  const isLast = stepIndex === steps.length - 1;

  return (
    <main className="max-w-3xl mx-auto px-6 py-8 w-full">
      <div className="mb-6">
        <Link href="/" className="text-sm text-muted-foreground hover:text-primary">
          ← {t(LABELS.backToList, locale)}
        </Link>
        <h1 className="text-2xl font-bold mt-2">
          <span className="font-mono text-primary">{fileName}</span>
          <span className="text-muted-foreground font-normal"> — {problemLabel}</span>
        </h1>
      </div>

      {/* Progress */}
      <div className="mb-6">
        <div className="flex items-center justify-between text-xs text-muted-foreground mb-2">
          <span>
            {t(LABELS.step, locale)} {stepIndex + 1} {t(LABELS.of, locale)} {steps.length}
          </span>
          <span>{t(step.title, locale)}</span>
        </div>
        <div className="flex gap-1">
          {steps.map((s, i) => (
            <button
              key={i}
              type="button"
              title={t(s.title, locale)}
              onClick={() => onStepChange(i)}
              className={
                "h-1.5 flex-1 rounded-full transition-colors " +
                (i < stepIndex ? "bg-primary/60" : i === stepIndex ? "bg-primary" : "bg-border")
              }
            />
          ))}
        </div>
      </div>

      <div className="bg-card rounded-2xl border shadow-sm p-6 space-y-4">
        <div>
          <h2 className="text-lg font-semibold text-primary border-l-[3px] border-primary pl-3">
            {t(step.title, locale)}
          </h2>
          <p className="text-sm text-muted-foreground mt-2 whitespace-pre-line">
            {t(step.guidance, locale)}
          </p>
        </div>
        {step.example && <ExampleBox example={step.example} />}
        {children}
        <div className="flex justify-between pt-4 border-t">
          <Button
            variant="outline"
            disabled={stepIndex === 0}
            onClick={() => onStepChange(stepIndex - 1)}
          >
            ← {t(LABELS.back, locale)}
          </Button>
          {!isLast && (
            <Button onClick={() => onStepChange(stepIndex + 1)}>
              {t(LABELS.next, locale)} →
            </Button>
          )}
        </div>
      </div>
    </main>
  );
}
