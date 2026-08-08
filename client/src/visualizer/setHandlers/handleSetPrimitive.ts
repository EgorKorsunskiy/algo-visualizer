import { CommandEntry, IndexedContainer, TIndex, TRange, TVisualize2DArray, TVisualizeArray } from "../types"

export type THandlerPrimitive = (
    entry: CommandEntry,
    _indexVars: IndexedContainer<TIndex>,
    _rangeVars: IndexedContainer<TRange>,
    _visualizeArray: TVisualizeArray | TVisualize2DArray
) => void

export const handleSetPrimitive: THandlerPrimitive = (entry, _indexVars, _rangeVars, _visualizeArray) => {
    if (!entry.var) return
    let currKey = entry.var
    for (const key of Object.keys(_rangeVars)) {
        if (key.includes(currKey)) {
            currKey = key
            break
        }
    }
    if (currKey !== entry.var) {
        const [firstComponent, secondComponent] = currKey.split("#")
        const rangeContent = _rangeVars[currKey].values.content as number[]
        if (firstComponent === entry.var) rangeContent[0] = entry.value as number
        else if (secondComponent === entry.var) rangeContent[1] = entry.value as number

        let start = Math.min(rangeContent[0], rangeContent[1])
        let end = Math.max(rangeContent[0], rangeContent[1])
        if ((start === -1 || end === -1) || (rangeContent[0] > rangeContent[1])) {
            start = end = -1
        }
        (_visualizeArray as TVisualizeArray)(
            _rangeVars[currKey].target,
            start,
            end,
            _rangeVars[currKey].values.color,
            true
        )
    }
    if (entry.var in _indexVars) {
        _indexVars[entry.var].value.content = entry.value as number
        const color = _indexVars[entry.var].value.color;
        (_visualizeArray as TVisualizeArray)(_indexVars[entry.var].target, entry.value as number, -1, color, true)
    }
}