"use client"
import { useAnalyzeProgramMutation } from "@/api/program";
import Canvas from "@/components/Canvas";
import { EditorWrapper } from "@/components/EditorWrapper";

export default function Home() {
  const { data, mutateAsync } = useAnalyzeProgramMutation()

  return (
    <div className="grid grid-cols-3 bg-zinc-50 font-sans min-h-screen">
      <div className="col-span-1">
        <EditorWrapper mutateFunc={mutateAsync} />
      </div>
      <div className="col-span-2">
        <Canvas logEntries={data || []} />
      </div>
    </div>
  );
}
