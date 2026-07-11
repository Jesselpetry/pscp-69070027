import fs from "fs";
import { reflectionTemplatePath, submissionTemplatePath } from "./paths";
import {
  SUBMISSION_BLOCK_FIELDS,
  SUBMISSION_CERT_STATEMENTS,
  REFLECTION_BLOCK_FIELDS,
  REFLECTION_INFO_ROWS,
  REFLECTION_POLICY_STATEMENTS,
  REFLECTION_CERT_STATEMENTS,
} from "./statements";

type Values = Record<string, unknown>;

function escapeRegExp(s: string) {
  return s.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
}

// Replaces the content of every ```text block in document order.
// null field = informational block, left untouched.
export function fillTextBlocks(
  template: string,
  fieldNames: (string | null)[],
  values: Values,
): string {
  const blocks = [...template.matchAll(/```text\n([\s\S]*?)\n```/g)];
  if (blocks.length !== fieldNames.length) {
    throw new Error("template block count changed, refusing to guess");
  }
  const out: string[] = [];
  let cursor = 0;
  blocks.forEach((block, i) => {
    const field = fieldNames[i];
    out.push(template.slice(cursor, block.index!));
    if (field === null) {
      out.push(block[0]);
    } else {
      const content = typeof values[field] === "string" ? (values[field] as string) : "";
      out.push("```text\n" + content + "\n```");
    }
    cursor = block.index! + block[0].length;
  });
  out.push(template.slice(cursor));
  return out.join("");
}

export function fillTwoColRow(text: string, label: string, value: string): string {
  const pattern = new RegExp(
    "^\\|[ \\t]*" + escapeRegExp(label) + "[ \\t]*\\|[^|\\n]*\\|[ \\t]*$",
    "m",
  );
  if (!pattern.test(text)) throw new Error(`row not found: ${label}`);
  return text.replace(pattern, `| ${label} | ${value} |`);
}

export function fillThreeColRow(text: string, label: string, value: string, note: string): string {
  const pattern = new RegExp(
    "^\\|[ \\t]*" + escapeRegExp(label) + "[ \\t]*\\|[^|\\n]*\\|[^|\\n]*\\|[ \\t]*$",
    "m",
  );
  if (!pattern.test(text)) throw new Error(`row not found: ${label}`);
  return text.replace(pattern, `| ${label} | ${value} | ${note} |`);
}

export function buildSubmissionMd(locale: "en" | "th", fields: Values): string {
  let text = fs.readFileSync(submissionTemplatePath(locale), "utf-8");
  text = fillTextBlocks(text, SUBMISSION_BLOCK_FIELDS, fields);
  const cert = (fields.certifications ?? {}) as Record<string, boolean>;
  for (const statement of SUBMISSION_CERT_STATEMENTS) {
    text = fillTwoColRow(text, statement, cert[statement] ? "Yes" : "");
  }
  return text;
}

export function buildReflectionMd(locale: "en" | "th", fields: Values): string {
  let text = fs.readFileSync(reflectionTemplatePath(locale), "utf-8");
  text = fillTextBlocks(text, REFLECTION_BLOCK_FIELDS, fields);
  const info = (fields.info ?? {}) as Record<string, string>;
  for (const label of REFLECTION_INFO_ROWS) {
    text = fillTwoColRow(text, label, info[label] ?? "");
  }
  const policy = (fields.policy ?? {}) as Record<string, { answer?: string; note?: string }>;
  for (const statement of REFLECTION_POLICY_STATEMENTS) {
    const row = policy[statement] ?? {};
    text = fillThreeColRow(text, statement, row.answer ?? "", row.note ?? "");
  }
  const cert = (fields.certifications ?? {}) as Record<string, boolean>;
  for (const statement of REFLECTION_CERT_STATEMENTS) {
    text = fillTwoColRow(text, statement, cert[statement] ? "Yes" : "");
  }
  return text;
}
