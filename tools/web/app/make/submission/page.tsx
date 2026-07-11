import { SubmissionWizard } from "@/components/submission-wizard";
import { Navbar } from "@/components/navbar";
import { loadProblems } from "@/lib/master";

export const dynamic = "force-dynamic";

export default async function MakeSubmission({
  searchParams,
}: {
  searchParams: Promise<{ problem?: string }>;
}) {
  const { problem } = await searchParams;
  const id = problem ?? "";
  const match = loadProblems().find((p) => String(p.id) === id);
  const ojTitle = match ? `OJ${match.id} - ${match.name}` : id ? `OJ${id}` : "";
  return (
    <>
      <Navbar />
      <SubmissionWizard problemId={id || "custom"} ojTitle={ojTitle} />
    </>
  );
}
