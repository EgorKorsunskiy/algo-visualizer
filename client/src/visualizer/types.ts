import { Wrapper } from "./wrapper"

export const RECORD_TYPE = {
    COMMAND: "COMMAND",
    HINT: "HINT",
} as const

export type RECORD_TYPE = keyof typeof RECORD_TYPE

export const COMMAND_TYPE = {
    SET: "SET",
    INSERT: "INSERT",
    UPDATE: "UPDATE",
    DELETE: "DELETE",
    FOR: "FOR",
    WHILE: "WHILE",
    IF: "IF",
    ELIF: "ELIF",
    ELSE: "ELSE",
} as const

export type COMMAND_TYPE = keyof typeof COMMAND_TYPE

export const HINT_TYPE = {
    INDEX: "INDEX",
    SELECT: "SELECT"
} as const

export type HINT_TYPE = keyof typeof HINT_TYPE

export const VAR_TYPE = {
    NONE: "NONE",
    PRIMITIVE: "PRIMITIVE",
    ARRAY: "ARRAY",
    ARRAY_2D: "ARRAY_2D",
    VECTOR: "VECTOR",
    VECTOR_2D: "VECTOR_2D",
    MAP: "MAP",
    GRAPH: "GRAPH"
} as const

export type VAR_TYPE = keyof typeof VAR_TYPE

export type CommandEntry = {
    recordType: typeof RECORD_TYPE.COMMAND
    commandType: COMMAND_TYPE
    varType: VAR_TYPE
    var: string | null
    value: null | string | number | boolean | Array<unknown>
    index: number
}

export type HintEntry = {
    recordType: typeof RECORD_TYPE.HINT
    hintType: HINT_TYPE
    target: string
    values: unknown[]
}

export type LogEntry = CommandEntry | HintEntry

export type TIndex = {
    target: string
    value: Wrapper
}

export type TRange = {
    target: string
    values: Wrapper
}

type coloringItem = number | Array<coloringItem>

export type IObject = {
    indexes: Record<string, Wrapper>
    ranges: Record<string, Wrapper>
    value: object
    colorsObject: Record<string, boolean>
    coloring: Array<Array<coloringItem>>
}

export type TVisualizeArray = (
    arrayKey: string,
    highlightStart?: number,
    highlightEnd?: number,
    color?: Array<number>,
    repaint?: boolean
) => void

export type TVisualize2DArray = (
    arrayKey: string,
    highlightStart?: Array<number>,
    highlightEnd?: Array<number>,
    color?: Array<number>,
    repaint?: boolean
) => void

export type IndexedContainer<T> = Record<string, T>
export interface IVisualizer {
    log: LogEntry[],
    canvas: HTMLCanvasElement,

    _gl: WebGLRenderingContext,
    _block_size: number
    _border_width: number

    _indexVars: IndexedContainer<TIndex>
    _rangeVars: IndexedContainer<TRange>
    _objects: IndexedContainer<IObject>,
    visualize: () => Promise<void>,
    _visualizeArray: TVisualizeArray,
    _visualize2DArray: TVisualize2DArray
}