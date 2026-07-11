import type { LText } from "./i18n";

// Guidance and example texts for each wizard step. Guidance follows the
// official templates in AI-Guidelines-PSCP/templates; examples are excerpts
// from AI-Guidelines-PSCP/examples (shown only to illustrate the expected
// level of detail — students must write their own words).

export const TIME_OPTIONS = [
  "0-15 minutes",
  "15-30 minutes",
  "30-60 minutes",
  "1-3 hours",
  "3-6 hours",
  "6-24 hours",
  "1-3 days",
  "4-7 days",
  "1-4 weeks",
  "More than 4 weeks",
];

export const HOW_TO_COUNT_TIME: LText = {
  th: `วิธีนับเวลา:
• นับเฉพาะเวลาที่ตั้งใจทำโจทย์นี้ด้วยตนเองจริง ๆ เริ่มตั้งแต่อ่านโจทย์ครั้งแรก
• ไม่นับเวลาพัก กินข้าว เรียน นอน หรือเวลาทำโจทย์อื่น
• ถ้าใช้ AI หรือถามคน ให้นับเฉพาะเวลาก่อนขอความช่วยเหลือจากภายนอกครั้งแรก
• ประมาณเวลาได้ แต่ต้องซื่อสัตย์`,
  en: `How to count this time:
• Count only the time you actively worked on this problem independently, starting from when you first read it.
• Do not include breaks, meals, classes, sleep, or time on other problems.
• If you used AI or asked a person, count only the independent time before the first outside help.
• An estimate is acceptable, but it must be honest.`,
};

export interface StepContent {
  title: LText;
  guidance: LText;
  example?: LText;
}

export const LANGUAGE_STEP: StepContent = {
  title: { th: "เลือกภาษาของไฟล์", en: "Choose the file language" },
  guidance: {
    th: "เลือกว่าไฟล์ที่จะสร้างใช้ template ภาษาไทยหรือภาษาอังกฤษ (เนื้อหาที่คุณพิมพ์จะถูกใส่ลงใน template ทางการของรายวิชาตามภาษาที่เลือก)",
    en: "Choose whether the generated file uses the Thai or English official template. Your own answers are inserted into the template of the language you pick.",
  },
};

export const SUBMISSION_STEPS: Record<string, StepContent> = {
  language: LANGUAGE_STEP,
  info: {
    title: { th: "1. ข้อมูล OJ", en: "1. OJ Information" },
    guidance: {
      th: "กรอกหมายเลข/ชื่อโจทย์ OJ, submission ID (ถ้ามี), สถานะจริงจากระบบ OJ และเวลาที่ใช้ทำด้วยตนเอง",
      en: "Fill in the OJ problem number/title, submission ID (if submitted), the real OJ status, and your independent time spent.",
    },
  },
  understanding: {
    title: { th: "2. ความเข้าใจโจทย์ของฉัน", en: "2. My Understanding" },
    guidance: {
      th: "เขียนโจทย์ด้วยคำพูดของตนเอง อธิบาย input, output และ constraints สำคัญ ถ้ายังไม่เข้าใจทั้งหมด ให้เขียนสิ่งที่เข้าใจตอนนี้อย่างจริงใจ",
      en: "Write the problem in your own words. Explain the input, output, and important constraints. If you do not fully understand yet, honestly write what you currently understand.",
    },
    example: {
      th: `โจทย์ให้ฉันอ่านจำนวนเต็มหนึ่งตัว แล้วตัดสินว่าเป็นเลขคู่หรือเลขคี่

Input:
โปรแกรมรับจำนวนเต็มหนึ่งค่า n

Output:
โปรแกรมควรพิมพ์ "Even" ถ้า n หารด้วย 2 ลงตัว มิฉะนั้นให้พิมพ์ "Odd"

Constraints:
input เป็นจำนวนเต็ม ฉันควรพิจารณา 0 และตัวเลขติดลบด้วย เพราะ modulo ยังใช้ได้ใน Python`,
      en: `The problem asks me to read n numbers and print their total sum.

Input:
The first line contains an integer n.
The next line contains n integers.

Output:
Print one integer, which is the sum of all n numbers.

Constraints:
I think n can be more than 1, so I should not write code for only one number. The numbers may include 0 or negative values, so the sum may decrease.`,
    },
  },
  first_plan: {
    title: { th: "3. แผนแรกของฉัน", en: "3. My First Plan" },
    guidance: {
      th: "เขียนแผนแรกก่อนรับความช่วยเหลือจาก AI เพื่อน TA ผู้สอน หรือก่อนสรุป code สุดท้าย เขียนคร่าว ๆ ได้ เป็น pseudocode, flowchart idea หรือขั้นตอนความคิด",
      en: "Write your first plan before getting help from AI, a friend, a TA, an instructor, or before finalizing your code. It can be rough — pseudocode, a flowchart idea, or step-by-step thinking.",
    },
    example: {
      th: `Step 1: อ่านจำนวนเต็ม n
Step 2: ตรวจว่า n % 2 == 0 หรือไม่
Step 3: ถ้าจริง ให้พิมพ์ "Even"
Step 4: ถ้าไม่จริง ให้พิมพ์ "Odd"

ก่อนถามเพื่อน ฉันรู้อยู่แล้วว่าควรใช้ modulo แต่ยังไม่แน่ใจว่าควร test ตัวเลขติดลบด้วยหรือไม่`,
      en: `Step 1: Read n
Step 2: Read numbers
Step 3: Use a loop to add each number to total
Step 4: Print total

At first, I was not sure whether the n numbers are always on one line or may be split across multiple lines.`,
    },
  },
  final_approach: {
    title: { th: "4. วิธีสุดท้ายที่ใช้จริง", en: "4. My Final Approach" },
    guidance: {
      th: "อธิบายสั้น ๆ ว่า algorithm หรือวิธีสุดท้ายที่ใช้จริงใน code ที่ส่งคืออะไร ถ้าเหมือนแผนแรก ให้เขียนว่าเหมือนและอธิบายสั้น ๆ ว่าทำไม ห้ามคัดลอกคำอธิบายจาก AI หรือคนอื่น",
      en: "Briefly explain the final algorithm actually used in your submitted code. If it is the same as your first plan, say so and briefly explain why. Do not copy AI's or another person's explanation.",
    },
    example: {
      th: "วิธีสุดท้ายของฉันเหมือนกับแผนแรก ฉันใช้ modulo เพื่อตรวจเศษเมื่อ n หารด้วย 2 ถ้าเศษเป็น 0 แสดงว่าเป็นเลขคู่ มิฉะนั้นเป็นเลขคี่ ฉันทดสอบ 0 และตัวเลขติดลบด้วยตนเองหลังจากเพื่อนเตือนว่า edge cases มีประโยชน์",
      en: "My final solution reads n first, then reads integers until it has n values. I used a running total variable and added each value one by one. This is close to my first plan, but I adjusted the input reading to handle the case where numbers may appear across multiple lines.",
    },
  },
  tests: {
    title: { th: "5. การทดสอบของฉัน", en: "5. My Tests" },
    guidance: {
      th: "เขียน test cases อย่างน้อย 3 กรณีที่ลองเองหรือออกแบบเอง พยายามเลือก case ที่แตกต่างกัน และอธิบายว่าทำไมเลือกแต่ละ case แนะนำ: case ปกติ, case เล็กสุด/ค่าพิเศษ (เช่น 0), และ case ที่อาจเจอความผิดพลาดที่พบบ่อย",
      en: "Write at least 3 test cases you tried or designed yourself. Choose cases that are different from each other and explain why you chose each one. Suggested: one normal case, one minimum/special value (e.g. 0), and one case that may reveal a common mistake.",
    },
    example: {
      th: `ทำไมเลือก case นี้: ตรวจค่า 0 เพราะ 0 เป็นค่าพิเศษ แต่ควรเป็นเลขคู่
Input: 0
Expected output: Even
Actual output: Even
Result: Pass`,
      en: `Why I chose this case: This checks whether my code works when the numbers are written on multiple lines.
Input:
6
1 2
3 4
5 6
Expected output: 21
Actual output: 21
Result: Pass`,
    },
  },
  ai_use: {
    title: { th: "6. การใช้ AI", en: "6. AI Use" },
    guidance: {
      th: "ตอบตามจริง ถ้าใช้ AI กับโจทย์นี้ และโจทย์เป็น learning-log-required ต้องทำไฟล์ ai_reflection.md ด้วย (เว็บนี้มีตัวช่วยสร้างให้)",
      en: "Answer honestly. If you used AI on this problem and it is learning-log-required, you must also complete ai_reflection.md (this site has a maker for it).",
    },
  },
  human_help: {
    title: { th: "7. ความช่วยเหลือจากคน / การร่วมมือ", en: "7. Human Help / Collaboration" },
    guidance: {
      th: `อนุญาต: อธิบายโจทย์, อธิบาย concept, hint แนวทาง, คุย debugging/test cases, ช่วยอธิบาย error message
ไม่อนุญาต: คัดลอก code ของผู้อื่น, ส่ง solution ของผู้อื่น, ขอให้ผู้อื่นเขียนหรือส่งแทน`,
      en: `Allowed: explanation of the problem or a concept, a hint about the approach, debugging / test-case discussion, help understanding an error message.
Not allowed: copying another person's code, submitting another person's solution, asking someone to write or submit for you.`,
    },
    example: {
      th: "ใครช่วยคุณ: เพื่อนร่วมชั้นหนึ่งคน\nเขาช่วยอะไร: เตือนว่าควรทดสอบ edge cases เช่น 0 และตัวเลขติดลบ\nคุณยังทำอะไรด้วยตนเอง: ฉันเขียนแผน เขียน code ทดสอบ และส่ง OJ ด้วยตนเองทั้งหมด",
      en: "Who helped you: No one.\nWhat did they help with: No human help was used.\nWhat did you still do by yourself: I wrote my own first plan, wrote and tested the final code in VS Code, designed my own test cases, and submitted to the OJ by myself.",
    },
  },
  declaration: {
    title: { th: "8. คำรับรองของนักศึกษา", en: "8. Student Declaration" },
    guidance: {
      th: "อ่านและติ๊กเฉพาะข้อที่เป็นจริง ถ้าข้อใดไม่จริง อย่าติ๊ก และกลับไปแก้ให้ถูกต้องก่อนส่ง",
      en: "Read and check only the statements that are true. If a statement is not true, do not check it — go back and fix your work first.",
    },
  },
  download: {
    title: { th: "เสร็จสิ้น — ดาวน์โหลด", en: "Finish — Download" },
    guidance: {
      th: "ตรวจตัวอย่างไฟล์ด้านล่าง แล้วดาวน์โหลด submission.md ไปวางในโฟลเดอร์โจทย์ของคุณ อย่าลืมตรวจอีกครั้งใน VS Code",
      en: "Review the preview below, then download submission.md into your problem folder. Remember to double-check it in VS Code.",
    },
  },
};

export const REFLECTION_STEPS: Record<string, StepContent> = {
  language: LANGUAGE_STEP,
  info: {
    title: { th: "1. ข้อมูล OJ", en: "1. OJ Information" },
    guidance: {
      th: "กรอกหมายเลข/ชื่อโจทย์ OJ, submission ID (ถ้ามี) และสถานะจริงจากระบบ OJ",
      en: "Fill in the OJ problem number/title, submission ID (if submitted), and the real OJ status.",
    },
  },
  tool: {
    title: { th: "2. เครื่องมือ AI ที่ใช้", en: "2. AI Tool Used" },
    guidance: {
      th: "เขียนชื่อเครื่องมือ AI ที่ใช้ เช่น ChatGPT, Claude, Gemini, Codex CLI, Claude Code",
      en: "Write the AI tool or tools you used, e.g. ChatGPT, Claude, Gemini, Codex CLI, Claude Code.",
    },
    example: { th: "Claude Code", en: "ChatGPT" },
  },
  policy: {
    title: {
      th: "3. การตรวจสอบนโยบายการใช้ AI ของรายวิชา",
      en: "3. Required Course AI Policy Check",
    },
    guidance: {
      th: "ตอบอย่างซื่อสัตย์ หัวข้อนี้ยืนยันว่าคุณทำตาม AI workflow ของรายวิชาก่อนและระหว่างใช้ AI ถ้าตอบ No ข้อใด ให้อธิบายเหตุผล",
      en: "Answer honestly. This section confirms you followed the course AI workflow before and while using AI. If you answer No to any item, explain why.",
    },
  },
  asked: {
    title: { th: "4. ฉันถาม AI ให้ช่วยอะไร", en: "4. What I Asked AI to Help With" },
    guidance: {
      th: "อธิบายสั้น ๆ ว่าถาม AI เรื่องอะไร ห้ามวาง chat log ทั้งหมด เช่น ให้ช่วยอธิบายโจทย์, review แผนแรก, หา bug, เสนอ test cases",
      en: "Briefly describe what you asked AI. Do not paste the full chat log. Examples: explain the problem, review my first plan, find a bug, suggest test cases.",
    },
    example: {
      th: "ฉันถาม AI ให้ช่วย review แผนแรกของฉันสำหรับการอ่านจำนวนเต็ม n ตัวและคำนวณผลรวม ฉันยังถามด้วยว่าวิธีอ่าน input ของฉันจะทำงานหรือไม่ ถ้าตัวเลขถูกแบ่งอยู่หลายบรรทัด",
      en: "I asked AI to review my first plan for reading n numbers and calculating their sum. I also asked whether my input-reading method would work if the numbers were split across multiple lines.",
    },
  },
  noticed: {
    title: { th: "5. AI ช่วยให้ฉันสังเกตอะไร", en: "5. What AI Helped Me Notice" },
    guidance: {
      th: "เช่น ความเข้าใจผิดเกี่ยวกับโจทย์, condition ที่ขาด, bug ในการอ่าน input, edge case, ปัญหา output formatting",
      en: "For example: a misunderstanding of the problem, a missing condition, a bug in input reading, an edge case, an output formatting problem.",
    },
    example: {
      th: "AI ช่วยให้ฉันสังเกตว่า ถ้าใช้ input().split() เพียงครั้งเดียว code อาจผิดเมื่อจำนวนเต็ม n ตัวถูกเขียนแยกหลายบรรทัด",
      en: "AI helped me notice that if I use input().split() only once, my code may fail when the n numbers are written across multiple lines.",
    },
  },
  checked: {
    title: {
      th: "6. ฉันตรวจสอบหรือแก้อะไรด้วยตนเอง",
      en: "6. What I Checked or Changed by Myself",
    },
    guidance: {
      th: "เขียนว่าคุณตรวจสอบ ทดสอบ หรือแก้อะไรเองหลังได้รับความช่วยเหลือจาก AI เช่น ตรวจ input format, ทดสอบใน VS Code, ไม่ใช้บางคำแนะนำเพราะไม่ตรง constraints",
      en: "Write what you verified, tested, or changed yourself after AI help — e.g. rechecked the input format, tested in VS Code, rejected a suggestion that did not match the constraints.",
    },
    example: {
      th: "ฉันกลับไปตรวจ problem statement ใน OJ อีกครั้ง และยืนยันว่า input อาจมีตัวเลขมากกว่าหนึ่งบรรทัด ฉันแก้ code ให้รับตัวเลขต่อไปจนกว่าจะได้จำนวนเต็มครบ n ค่า",
      en: "I checked the OJ problem statement again and confirmed that the input may contain numbers on more than one line. I changed my code to keep reading until it had n integers, then tested three different cases.",
    },
  },
  learned: {
    title: { th: "7. ฉันได้เรียนรู้อะไร", en: "7. What I Learned" },
    guidance: {
      th: 'เขียน 2-4 ประโยคเกี่ยวกับสิ่งที่เรียนรู้ เน้นการเรียนรู้ของตนเอง ห้ามเขียนแค่ "I learned coding" หรือ "AI helped me."',
      en: 'Write 2-4 sentences about what you learned. Focus on your own learning. Do not write only "I learned coding" or "AI helped me."',
    },
    example: {
      th: "ฉันได้เรียนรู้ว่า input format สำคัญ และตัวเลขอาจไม่ได้อยู่ในบรรทัดเดียวเสมอ AI มีประโยชน์ในการชี้ให้เห็น bug แต่ฉันยังต้องตรวจสอบด้วย test cases ของตนเอง",
      en: "I learned that input format is important and that numbers may not always appear on one line. AI was useful for pointing out a possible input-reading bug, but I still had to verify it with my own tests.",
    },
  },
  declaration: {
    title: { th: "8. คำรับรองของนักศึกษา", en: "8. Student Declaration" },
    guidance: {
      th: "อ่านและติ๊กเฉพาะข้อที่เป็นจริง",
      en: "Read and check only the statements that are true.",
    },
  },
  download: {
    title: { th: "เสร็จสิ้น — ดาวน์โหลด", en: "Finish — Download" },
    guidance: {
      th: "ตรวจตัวอย่างไฟล์ด้านล่าง แล้วดาวน์โหลด ai_reflection.md ไปวางในโฟลเดอร์โจทย์ของคุณ",
      en: "Review the preview below, then download ai_reflection.md into your problem folder.",
    },
  },
};
