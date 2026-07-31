"use client"
import { Visualizer } from "@/visualizer"
import { useLayoutEffect, useRef } from "react"
import { TCanvasProps } from "./types"

export default function Canvas({ logEntries }: TCanvasProps) {
    const ref = useRef<HTMLCanvasElement | null>(null)

    useLayoutEffect(() => {
        if (ref.current === null) return
        const visualizer = new Visualizer(logEntries, ref.current)
        visualizer.visualize()
    }, [])

    return (
        <canvas className="w-full h-full" ref={ref}></canvas>
    )
}
