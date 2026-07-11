"use client";

import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";

export function SectionTitle({ children }: { children: React.ReactNode }) {
  return (
    <h4 className="mt-6 mb-2 text-primary font-semibold border-l-[3px] border-primary pl-2">
      {children}
    </h4>
  );
}

export function TextField({
  label,
  hint,
  value,
  onChange,
  rows = 3,
}: {
  label: string;
  hint?: string;
  value: string;
  onChange: (v: string) => void;
  rows?: number;
}) {
  return (
    <div className="space-y-1.5">
      <Label className="text-muted-foreground">{label}</Label>
      {hint && <p className="text-xs text-muted-foreground/80">{hint}</p>}
      <Textarea value={value} onChange={(e) => onChange(e.target.value)} rows={rows} />
    </div>
  );
}

export type BadgeTone = "green" | "red" | "gray" | "amber" | "primary";

const ACTIVE_TONE: Record<BadgeTone, string> = {
  green: "border-emerald-500 bg-emerald-500 text-white",
  red: "border-red-500 bg-red-500 text-white",
  gray: "border-slate-400 bg-slate-400 text-white dark:border-slate-500 dark:bg-slate-500",
  amber: "border-amber-500 bg-amber-500 text-white",
  primary: "border-primary bg-primary text-primary-foreground",
};

// Badge-style single choice (replaces dropdowns). Colors per option via `colors`.
export function ChoiceBadges({
  label,
  value,
  onChange,
  options,
  colors,
}: {
  label: string;
  value: string;
  onChange: (v: string) => void;
  options: string[];
  colors?: Record<string, BadgeTone>;
}) {
  return (
    <div className="space-y-1.5">
      {label && <Label className="text-muted-foreground">{label}</Label>}
      <div className="flex flex-wrap gap-2">
        {options.map((o) => {
          const active = value === o;
          const tone = colors?.[o] ?? "primary";
          return (
            <button
              key={o}
              type="button"
              onClick={() => onChange(o)}
              className={
                "rounded-full border px-4 py-1.5 text-sm font-medium transition-colors " +
                (active
                  ? ACTIVE_TONE[tone]
                  : "border-border bg-background text-muted-foreground hover:border-primary/50 hover:text-foreground")
              }
            >
              {active ? "✓ " : ""}
              {o}
            </button>
          );
        })}
      </div>
    </div>
  );
}

export function SelectField({
  label,
  value,
  onChange,
  options,
}: {
  label: string;
  value: string;
  onChange: (v: string) => void;
  options: string[];
}) {
  return (
    <div className="space-y-1.5">
      <Label className="text-muted-foreground">{label}</Label>
      <Select value={value} onValueChange={onChange}>
        <SelectTrigger className="w-full">
          <SelectValue />
        </SelectTrigger>
        <SelectContent>
          {options.map((o) => (
            <SelectItem key={o} value={o}>
              {o}
            </SelectItem>
          ))}
        </SelectContent>
      </Select>
    </div>
  );
}
