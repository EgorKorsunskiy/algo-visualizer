import { PropsWithChildren } from "react";
import type { CommandEntry, HintEntry } from "@/visualizer/types";

const LogContainer = ({ children }: PropsWithChildren) => {
    return (
        <div className='flex gap-3 items-center text-black'>
            {children}
        </div>
    )
}

export const CommandEntryWrapper = ({ recordType, commandType, varType, var: varName, value, index }: CommandEntry) => {
    return (
        <LogContainer>
            <p>{recordType}</p>
            <p>{commandType}</p>
            <p>{varType}</p>
            <p>{varName}</p>
            <p>{value?.toString()}</p>
            <p>{index}</p>
        </LogContainer>
    )
}

export const HintEntryWrapper = ({ recordType, hintType, target, values }: HintEntry) => {
    return (
        <LogContainer>
            <p>{recordType}</p>
            <p>{hintType}</p>
            <p>{target}</p>
            <p>{values.toString()}</p>
        </LogContainer>
    )
}