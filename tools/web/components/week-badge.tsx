import { Badge } from "@/components/ui/badge";
import { cn } from "@/lib/utils";

// Cycle of soft badge palettes; week N picks (N-1) mod length.
const WEEK_STYLES = [
  "bg-sky-100 text-sky-700 border-sky-200 dark:bg-sky-950 dark:text-sky-300 dark:border-sky-900",
  "bg-violet-100 text-violet-700 border-violet-200 dark:bg-violet-950 dark:text-violet-300 dark:border-violet-900",
  "bg-amber-100 text-amber-700 border-amber-200 dark:bg-amber-950 dark:text-amber-300 dark:border-amber-900",
  "bg-emerald-100 text-emerald-700 border-emerald-200 dark:bg-emerald-950 dark:text-emerald-300 dark:border-emerald-900",
  "bg-rose-100 text-rose-700 border-rose-200 dark:bg-rose-950 dark:text-rose-300 dark:border-rose-900",
  "bg-indigo-100 text-indigo-700 border-indigo-200 dark:bg-indigo-950 dark:text-indigo-300 dark:border-indigo-900",
];

export function WeekBadge({ week, className }: { week: number; className?: string }) {
  const style = WEEK_STYLES[(week - 1) % WEEK_STYLES.length];
  return (
    <Badge variant="outline" className={cn("font-semibold", style, className)}>
      Week {week}
    </Badge>
  );
}
