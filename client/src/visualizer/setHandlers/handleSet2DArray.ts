import { COLORS } from "@/webgl/helpers/constants"
import { createColosObject } from "../helpers"
import { THandlerArray } from "./handleSetArray"

export const handleSet2DArray: THandlerArray = (entry, _objects, _visualizeArray) => {
    if (!entry.var || !entry.value) return
    _objects[entry.var] = { value: [], indexes: {}, ranges: {}, colorsObject: {}, coloring: [] }
    _objects[entry.var].value = entry.value as object
    _objects[entry.var].colorsObject = createColosObject()
    const coloring = []
    for (const row of entry.value as Array<Array<unknown>>) {
        coloring.push((new Array(row.length)).fill(COLORS.BLUE))
    }
    _objects[entry.var].coloring = coloring
    _visualizeArray(entry.var)
}