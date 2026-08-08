import { COLORS } from "@/webgl/helpers/constants";
import { THandlerArray } from "../setHandlers/handleSetArray";
import { TVisualizeArray } from "../types";

export const handleInsertArray: THandlerArray = (entry, _objects, _visualizeArray) => {
    if (!entry.var || !entry.value) return
    const currValue = _objects[entry.var].value as Array<unknown>

    currValue[entry.index] = entry.value
    _objects[entry.var].coloring[entry.index] = COLORS.YELLOW;
    (_visualizeArray as TVisualizeArray)(entry.var, entry.index, -1, COLORS.YELLOW, true)
}