"use client"
import { Visualizer } from "@/visualizer"
import { COMMAND_TYPE, HINT_TYPE, RECORD_TYPE, VAR_TYPE } from "@/visualizer/types"
import { useLayoutEffect, useRef } from "react"

const MOCK_DATA = [
    {
        recordType: RECORD_TYPE.COMMAND,
        commandType: COMMAND_TYPE.SET,
        varType: VAR_TYPE.ARRAY,
        var: "v",
        value: [1, 2, 3, 4, 5, 8, 9, 11],
        index: -1,
    },
    {
        recordType: RECORD_TYPE.HINT,
        hintType: HINT_TYPE.SELECT,
        target: "v",
        values: ["low", "high"],
    },
    {
        recordType: RECORD_TYPE.COMMAND,
        commandType: COMMAND_TYPE.SET,
        varType: VAR_TYPE.PRIMITIVE,
        var: "low",
        value: 0,
        index: -1,
    },
    {
        recordType: RECORD_TYPE.HINT,
        hintType: HINT_TYPE.INDEX,
        target: "v",
        values: ['mid'],
    },
    {
        recordType: RECORD_TYPE.COMMAND,
        commandType: COMMAND_TYPE.SET,
        varType: VAR_TYPE.PRIMITIVE,
        var: "high",
        value: 9,
        index: -1,
    },
    {
        recordType: RECORD_TYPE.COMMAND,
        commandType: COMMAND_TYPE.WHILE,
        varType: VAR_TYPE.NONE,
        var: null,
        value: null,
        index: -1,
    },
    {
        recordType: RECORD_TYPE.COMMAND,
        commandType: COMMAND_TYPE.SET,
        varType: VAR_TYPE.PRIMITIVE,
        var: "mid",
        value: 4,
        index: -1,
    },
    {
        recordType: RECORD_TYPE.COMMAND,
        commandType: COMMAND_TYPE.ELSE,
        varType: VAR_TYPE.NONE,
        var: null,
        value: null,
        index: -1,
    },
    {
        recordType: RECORD_TYPE.COMMAND,
        commandType: COMMAND_TYPE.ELSE,
        varType: VAR_TYPE.NONE,
        var: null,
        value: null,
        index: -1,
    },
    {
        recordType: RECORD_TYPE.COMMAND,
        commandType: COMMAND_TYPE.SET,
        varType: VAR_TYPE.PRIMITIVE,
        var: "low",
        value: 5,
        index: -1,
    },
    {
        recordType: RECORD_TYPE.COMMAND,
        commandType: COMMAND_TYPE.SET,
        varType: VAR_TYPE.PRIMITIVE,
        var: "mid",
        value: 7,
        index: -1,
    },
    {
        recordType: RECORD_TYPE.COMMAND,
        commandType: COMMAND_TYPE.ELSE,
        varType: VAR_TYPE.NONE,
        var: null,
        value: null,
        index: -1,
    },
    {
        recordType: RECORD_TYPE.COMMAND,
        commandType: COMMAND_TYPE.IF,
        varType: VAR_TYPE.NONE,
        var: null,
        value: null,
        index: -1,
    },
    {
        recordType: RECORD_TYPE.COMMAND,
        commandType: COMMAND_TYPE.SET,
        varType: VAR_TYPE.PRIMITIVE,
        var: "high",
        value: 6,
        index: -1,
    },
    {
        recordType: RECORD_TYPE.COMMAND,
        commandType: COMMAND_TYPE.SET,
        varType: VAR_TYPE.PRIMITIVE,
        var: "mid",
        value: 5,
        index: -1,
    },
    {
        recordType: RECORD_TYPE.COMMAND,
        commandType: COMMAND_TYPE.ELSE,
        varType: VAR_TYPE.NONE,
        var: null,
        value: null,
        index: -1,
    },
    {
        recordType: RECORD_TYPE.COMMAND,
        commandType: COMMAND_TYPE.ELSE,
        varType: VAR_TYPE.NONE,
        var: null,
        value: null,
        index: -1,
    },
    {
        recordType: RECORD_TYPE.COMMAND,
        commandType: COMMAND_TYPE.SET,
        varType: VAR_TYPE.PRIMITIVE,
        var: "low",
        value: 6,
        index: -1,
    },
    {
        recordType: RECORD_TYPE.COMMAND,
        commandType: COMMAND_TYPE.SET,
        varType: VAR_TYPE.PRIMITIVE,
        var: "mid",
        value: 6,
        index: -1,
    },
    {
        recordType: RECORD_TYPE.COMMAND,
        commandType: COMMAND_TYPE.IF,
        varType: VAR_TYPE.NONE,
        var: null,
        value: null,
        index: -1,
    },
    {
        recordType: RECORD_TYPE.COMMAND,
        commandType: COMMAND_TYPE.ELSE,
        varType: VAR_TYPE.NONE,
        var: null,
        value: null,
        index: -1,
    },
    {
        recordType: RECORD_TYPE.COMMAND,
        commandType: COMMAND_TYPE.SET,
        varType: VAR_TYPE.PRIMITIVE,
        var: "low",
        value: 7,
        index: -1,
    },
]

export default function Canvas() {
    const ref = useRef<HTMLCanvasElement | null>(null)

    useLayoutEffect(() => {
        if (ref.current === null) return
        const visualizer = new Visualizer(MOCK_DATA, ref.current)
        visualizer.visualize()
    }, [])

    return (
        <canvas className="w-full h-full" ref={ref}></canvas>
    )
}
