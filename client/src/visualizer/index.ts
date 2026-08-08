import { drawOutlinedRectangle } from "@/webgl/helpers/drawShapes";
import { COMMAND_TYPE, HINT_TYPE, IObject, TRange, IVisualizer, LogEntry, RECORD_TYPE, TIndex, VAR_TYPE } from "./types";
import { COLORS } from "@/webgl/helpers/constants";
import { resizeCanvas } from "@/webgl/helpers/initProgram";
import { Wrapper } from "./wrapper";
import { compareArrays } from "./helpers";
import { handleSetArray } from "./setHandlers/handleSetArray";
import { handleSet2DArray } from "./setHandlers/handleSet2DArray";
import { handleSetPrimitive } from "./setHandlers/handleSetPrimitive";
import { handleInsertArray } from "./insertHandlers/handleInsertArray";

export class Visualizer implements IVisualizer {
    log
    canvas

    _gl
    _block_size = 100
    _border_width = 10

    _indexVars: Record<string, TIndex> = {}
    _rangeVars: Record<string, TRange> = {}
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
                                    handleSetArray(entry, this._objects, this._visualizeArray.bind(this))
                                    break
                                case VAR_TYPE.ARRAY_2D:
                                    handleSet2DArray(entry, this._objects, this._visualize2DArray.bind(this))
                                    break
                                case VAR_TYPE.VECTOR:
                                    handleSetArray(entry, this._objects, this._visualizeArray.bind(this))
                                    break
                                case VAR_TYPE.VECTOR_2D:
                                    handleSet2DArray(entry, this._objects, this._visualize2DArray.bind(this))
                                    break
                                case VAR_TYPE.PRIMITIVE:
                                    handleSetPrimitive(entry, this._indexVars, this._rangeVars, this._visualizeArray.bind(this))
                                    break
                            }
                            break
                        case COMMAND_TYPE.INSERT:
                            switch (entry.varType) {
                                case VAR_TYPE.VECTOR:
                                    handleInsertArray(entry, this._objects, this._visualizeArray.bind(this))
                                    break
                            }
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
    _visualizeArray(arrayKey: string, highlightStart = -1, highlightEnd = -1, color = COLORS.RED, repaint = false) {
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
                    coloring[indx] as Array<number>,
                    this._border_width,
                    String(item)
                )
            }
            currentX += this._block_size + this._border_width
        }
    }

    _visualize2DArray(
        arrayKey: string,
        highlightStart = [-1, -1],
        highlightEnd = [-1, -1],
        color = COLORS.RED,
        repaint = false
    ) {
        const array = this._objects[arrayKey].value as Array<Array<unknown>>
        const coloring = this._objects[arrayKey].coloring
        if (highlightStart.every(x => x != 1) && highlightEnd.every(x => x == -1)) highlightEnd = highlightStart
        const initialX = this.canvas.width / 2 - (array.length / 2) * this._block_size
        let currentX = initialX
        let currentY = this.canvas.height / 2 - this._block_size / 2
        for (const [rowIndx, row] of array.entries()) {
            for (const [colIndx, col] of row.entries()) {
                const inRange = (highlightStart[0] <= rowIndx && rowIndx <= highlightEnd[0]) && (highlightStart[1] <= colIndx && colIndx <= highlightEnd[1])
                if ((!repaint || inRange) || (repaint && !inRange && compareArrays(coloring[rowIndx][colIndx] as Array<number>, color))) {
                    coloring[rowIndx][colIndx] = inRange ? color : COLORS.BLUE
                    drawOutlinedRectangle(
                        this._gl,
                        currentX,
                        currentY,
                        this._block_size,
                        this._block_size,
                        coloring[rowIndx][colIndx] as Array<number>,
                        this._border_width,
                        String(col)
                    )
                }
                currentX += this._block_size + this._border_width
            }
            currentX = initialX
            currentY += this._block_size + this._border_width
        }
    }
}