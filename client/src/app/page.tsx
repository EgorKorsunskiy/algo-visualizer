import Canvas from "@/components/Canvas";
import { EditorWrapper } from "@/components/EditorWrapper";

export default function Home() {
  return (
    <div className="grid grid-cols-3 bg-zinc-50 font-sans min-h-screen">
      <div className="col-span-1">
        <EditorWrapper />
      </div>
      <div className="col-span-2">
        <Canvas />
      </div>
    </div>
  );
}
