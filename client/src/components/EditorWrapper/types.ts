import { TRecordLog } from "@/api/program/types"
import { LogEntry } from "@/visualizer/types"
import { UseMutateAsyncFunction } from "@tanstack/react-query"

export type TEditorWrapperProps = {
    logEntries: LogEntry[]
    mutateFunc: UseMutateAsyncFunction<TRecordLog[], Error, string, unknown>
}