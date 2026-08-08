import { COLORS } from "@/webgl/helpers/constants"
import { createColosObject } from "../helpers"
import { CommandEntry, IObject, TVisualize2DArray, TVisualizeArray } from "../types"

export type THandlerArray = (
    entry: CommandEntry,
    _objects: Record<string, IObject>,
    _visualizeArray: TVisualizeArray | TVisualize2DArray
) => void

export const handleSetArray: THandlerArray = (entry, _objects, _visualizeArray) => {
    if (!entry.var || !entry.value) return
    _objects[entry.var] = { value: [], indexes: {}, ranges: {}, colorsObject: {}, coloring: [] }
    _objects[entry.var].value = entry.value as object
    _objects[entry.var].colorsObject = createColosObject()
    _objects[entry.var].coloring = (new Array((entry.value as Array<unknown>).length)).fill(COLORS.BLUE)
    _visualizeArray(entry.var)
}