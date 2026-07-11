// Shared between server (template filling) and client (form rendering).

export const SUBMISSION_BLOCK_FIELDS: (string | null)[] = [
  "oj_title", "submission_id", "oj_status", "time_spent", null,
  "understanding", "first_plan", "final_approach",
  "t1_why", "t1_input", "t1_expected", "t1_actual", "t1_result",
  "t2_why", "t2_input", "t2_expected", "t2_actual", "t2_result",
  "t3_why", "t3_input", "t3_expected", "t3_actual", "t3_result",
  "used_ai", null,
  "human_help", "who_helped", "what_help", "still_own_work", "copied_code",
];

export const SUBMISSION_CERT_STATEMENTS = [
  "I wrote this submission in my own words.",
  "I understand my final code.",
  "I recorded the real OJ status.",
  "I did not copy AI-generated text directly into this file.",
  "I did not copy code from another person.",
  "If I received human help, I disclosed it in this file.",
  "I submitted the final code to the OJ by myself.",
];

export const REFLECTION_BLOCK_FIELDS: (string | null)[] = [
  null, null,
  "ai_tool", "policy_no_explain", "what_asked", "what_noticed",
  "what_checked", "what_learned",
];

export const REFLECTION_INFO_ROWS = [
  "OJ problem number/title",
  "OJ submission ID, if submitted",
  "OJ status",
];

export const REFLECTION_POLICY_STATEMENTS = [
  "I read the relevant workflow before using AI.",
  "I used `instructions/COURSE_AI_INSTRUCTIONS.md`, `instructions/AGENTS.md`, or manually followed the course AI instructions if the tool did not support custom instructions.",
  "I wrote my own problem understanding before asking AI for help.",
  "I wrote my own first plan before asking AI for help.",
  "I used AI as a coach, reviewer, debugger, or test-case helper, not as a full-answer generator.",
];

export const REFLECTION_CERT_STATEMENTS = [
  "I wrote this reflection in my own words.",
  "This reflection describes my real AI use.",
  "I checked AI's suggestions before using them.",
  "I can explain my final code.",
  "I did not ask AI to write this reflection for me.",
];

// Thai display versions of the statements above. The generated markdown
// always keeps the English originals (the official template tables match
// those exact strings); these are shown in the UI when locale = th.
export const STATEMENT_TH: Record<string, string> = {
  // submission declaration
  "I wrote this submission in my own words.":
    "ฉันเขียน submission นี้ด้วยคำพูดของตนเอง",
  "I understand my final code.":
    "ฉันเข้าใจ code สุดท้ายของตนเอง",
  "I recorded the real OJ status.":
    "ฉันบันทึกสถานะ OJ ตามจริง",
  "I did not copy AI-generated text directly into this file.":
    "ฉันไม่ได้คัดลอกข้อความที่ AI สร้างมาใส่ไฟล์นี้โดยตรง",
  "I did not copy code from another person.":
    "ฉันไม่ได้คัดลอก code จากผู้อื่น",
  "If I received human help, I disclosed it in this file.":
    "หากได้รับความช่วยเหลือจากคน ฉันได้เปิดเผยไว้ในไฟล์นี้แล้ว",
  "I submitted the final code to the OJ by myself.":
    "ฉันส่ง code สุดท้ายเข้าระบบ OJ ด้วยตนเอง",
  // reflection policy check
  "I read the relevant workflow before using AI.":
    "ฉันได้อ่าน workflow ที่เกี่ยวข้องก่อนใช้ AI",
  "I used `instructions/COURSE_AI_INSTRUCTIONS.md`, `instructions/AGENTS.md`, or manually followed the course AI instructions if the tool did not support custom instructions.":
    "ฉันใช้ `instructions/COURSE_AI_INSTRUCTIONS.md`, `instructions/AGENTS.md` หรือทำตามคำแนะนำการใช้ AI ของรายวิชาด้วยตนเอง หากเครื่องมือไม่รองรับ custom instructions",
  "I wrote my own problem understanding before asking AI for help.":
    "ฉันเขียนความเข้าใจโจทย์ของตนเองก่อนขอความช่วยเหลือจาก AI",
  "I wrote my own first plan before asking AI for help.":
    "ฉันเขียนแผนแรกของตนเองก่อนขอความช่วยเหลือจาก AI",
  "I used AI as a coach, reviewer, debugger, or test-case helper, not as a full-answer generator.":
    "ฉันใช้ AI เป็น coach, reviewer, debugger หรือผู้ช่วยคิด test case ไม่ใช่เครื่องสร้างคำตอบสำเร็จรูป",
  // reflection declaration
  "I wrote this reflection in my own words.":
    "ฉันเขียน reflection นี้ด้วยคำพูดของตนเอง",
  "This reflection describes my real AI use.":
    "reflection นี้อธิบายการใช้ AI จริงของฉัน",
  "I checked AI's suggestions before using them.":
    "ฉันตรวจสอบคำแนะนำของ AI ก่อนนำมาใช้",
  "I can explain my final code.":
    "ฉันสามารถอธิบาย code สุดท้ายของตนเองได้",
  "I did not ask AI to write this reflection for me.":
    "ฉันไม่ได้ให้ AI เขียน reflection นี้แทน",
};

export function statementLabel(statement: string, locale: "th" | "en"): string {
  return locale === "th" ? STATEMENT_TH[statement] ?? statement : statement;
}

export const MAIN_PY_TEMPLATE = `def main():
    pass


if __name__ == "__main__":
    main()
`;
