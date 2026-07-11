import { NextResponse } from "next/server";
import { buildReflectionMd } from "@/lib/markdown";

export async function POST(req: Request) {
  try {
    const { locale, fields } = await req.json();
    const md = buildReflectionMd(locale === "en" ? "en" : "th", fields ?? {});
    return NextResponse.json({ markdown: md });
  } catch (e) {
    return NextResponse.json({ error: (e as Error).message }, { status: 400 });
  }
}
