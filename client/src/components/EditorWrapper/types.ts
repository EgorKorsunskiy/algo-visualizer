import { TRecordLog } from "@/api/program/types"
import { UseMutateAsyncFunction } from "@tanstack/react-query"

export type TEditorWrapperProps = {
    mutateFunc: UseMutateAsyncFunction<TRecordLog[], Error, string, unknown>
}