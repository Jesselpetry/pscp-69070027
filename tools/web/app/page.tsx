import { Navbar } from "@/components/navbar";
import { ProblemsView } from "@/components/problems-view";
import { loadProblems } from "@/lib/master";

export const dynamic = "force-dynamic";

export default function Home() {
  return (
    <>
      <Navbar />
      <ProblemsView problems={loadProblems()} />
    </>
  );
}
