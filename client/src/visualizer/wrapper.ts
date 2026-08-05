import { getAvailableColor } from "./helpers"

export class Wrapper {
    content: number | Array<number>
    color: Array<number>

    constructor(content: number | Array<number>, colorsObject: Record<string, boolean>) {
        this.content = content
        this.color = getAvailableColor(colorsObject)
    }
}