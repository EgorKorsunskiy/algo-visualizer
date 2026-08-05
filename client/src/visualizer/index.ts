import { drawOutlinedRectangle } from "@/webgl/helpers/drawShapes";
import { COMMAND_TYPE, HINT_TYPE, IObject, IRange, LogEntry, RECORD_TYPE, TIndex, VAR_TYPE } from "./types";
import { COLORS } from "@/webgl/helpers/constants";
import { resizeCanvas } from "@/webgl/helpers/initProgram";
import { Wrapper } from "./wrapper";
import { compareArrays, createColosObject } from "./helpers";

export class Visualizer {
    log: LogEntry[]
    canvas: HTMLCanvasElement

    _gl: WebGLRenderingContext
    _block_size = 100
    _border_width = 10

    _indexVars: Record<string, TIndex> = {}
    _rangeVars: Record<string, IRange> = {}
    _objects: Record<string, IObject> = {}

    constructor(log: LogEntry[], canvas: HTMLCanvasElement) {
        this.log = log
        this.canvas = canvas
        const gl = canvas.getContext("webgl", { preserveDrawingBuffer: true }) as WebGLRenderingContext
        if (gl === null) {
            console.warn("Unable to initialize WebGL. Your browser or machine may not support it.")
        }
        resizeCanvas(gl)
        this._gl = gl
    }
    async visualize() {
        // TODO: refactor it to reduce nesting
        for (const entry of this.log) {
            await new Promise((resolve) => setTimeout(resolve, 500))
            switch (entry.recordType) {
                case RECORD_TYPE.COMMAND:
                    switch (entry.commandType) {
                        case COMMAND_TYPE.SET:
                            switch (entry.varType) {
                                case VAR_TYPE.ARRAY:
                                    if (!entry.var || !entry.value) continue
                                    this._objects[entry.var] = { value: [], indexes: {}, ranges: {}, colorsObject: {}, coloring: [] }
                                    this._objects[entry.var].value = entry.value as object
                                    this._objects[entry.var].colorsObject = createColosObject()
                                    this._objects[entry.var].coloring = (new Array((entry.value as Array<unknown>).length)).fill(COLORS.BLUE)
                                    this._visualizeArray(entry.var)
                                    break
                                case VAR_TYPE.PRIMITIVE:
                                    if (!entry.var) break
                                    let currKey = entry.var
                                    for (const key of Object.keys(this._rangeVars)) {
                                        if (key.includes(currKey)) {
                                            currKey = key
                                            break
                                        }
                                    }
                                    if (currKey !== entry.var) {
                                        const [firstComponent, secondComponent] = currKey.split("#")
                                        const rangeContent = this._rangeVars[currKey].values.content as number[]
                                        if (firstComponent === entry.var) rangeContent[0] = entry.value as number
                                        else if (secondComponent === entry.var) rangeContent[1] = entry.value as number
                                        console.log(rangeContent)
                                        let start = Math.min(rangeContent[0], rangeContent[1])
                                        let end = Math.max(rangeContent[0], rangeContent[1])
                                        if ((start === -1 || end === -1) || (rangeContent[0] > rangeContent[1])) {
                                            start = end = -1
                                        }
                                        this._visualizeArray(
                                            this._rangeVars[currKey].target,
                                            start,
                                            end,
                                            this._rangeVars[currKey].values.color,
                                            true
                                        )
                                    }
                                    if (entry.var in this._indexVars) {
                                        this._indexVars[entry.var].value.content = entry.value as number
                                        const color = this._indexVars[entry.var].value.color
                                        this._visualizeArray(this._indexVars[entry.var].target, entry.value as number, -1, color, true)
                                    }
                            }
                            break
                    }
                    break
                case RECORD_TYPE.HINT:
                    switch (entry.hintType) {
                        case HINT_TYPE.INDEX:
                            if (entry.values.length < 1) {
                                console.warn("Invalid format for INDEX hint")
                                continue
                            }
                            const indexColorsObject = this._objects[entry.target].colorsObject
                            const indexSource = entry.values[0] as string
                            const indexWrapper = new Wrapper(-1, indexColorsObject)
                            this._indexVars[indexSource] = { target: entry.target, value: indexWrapper }
                            this._objects[entry.target].indexes[indexSource] = indexWrapper
                            break
                        case HINT_TYPE.SELECT:
                            if (entry.values.length < 2) {
                                console.warn("Invalid format for INDEX hint")
                                continue
                            }
                            const selectColorsObject = this._objects[entry.target].colorsObject
                            const selectSourceFirst = entry.values[0] as string
                            const selectSourceSecond = entry.values[1] as string
                            const selectKey = `${selectSourceFirst}#${selectSourceSecond}`
                            const selectWrapper = new Wrapper([-1, -1], selectColorsObject)
                            this._rangeVars[selectKey] = { target: entry.target, values: selectWrapper }
                            this._objects[entry.target].ranges[selectKey] = selectWrapper
                            break
                    }
                    break
            }
        }
    }
    _visualizeArray(arrayKey: string, highlightStart: number = -1, highlightEnd: number = -1, color: Array<number> = COLORS.RED, repaint: boolean = false) {
        const array = this._objects[arrayKey].value as Array<unknown>
        const coloring = this._objects[arrayKey].coloring
        if (highlightStart != -1 && highlightEnd == -1) highlightEnd = highlightStart
        let currentX = this.canvas.width / 2 - (array.length / 2) * this._block_size
        const currentY = this.canvas.height / 2 - this._block_size / 2
        for (const [indx, item] of array.entries()) {
            const inRange = (highlightStart <= indx && indx <= highlightEnd)
            if ((!repaint || inRange) || (repaint && !inRange && compareArrays(coloring[indx], color))) {
                coloring[indx] = inRange ? color : COLORS.BLUE
                drawOutlinedRectangle(
                    this._gl,
                    currentX,
                    currentY,
                    this._block_size,
                    this._block_size,
                    coloring[indx],
                    this._border_width,
                    String(item)
                )
            }
            currentX += this._block_size + this._border_width
        }
    }
}