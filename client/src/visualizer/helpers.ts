import { COLORS } from "@/webgl/helpers/constants";

const colorsSingleton = Object.fromEntries(Object.keys(COLORS).map(key => [key, true]))

export function getAvailableColor() {
    for (const key of Object.keys(colorsSingleton)) {
        if (colorsSingleton[key]) {
            colorsSingleton[key] = false
            return COLORS[key as keyof typeof COLORS]
        }
    }
    return COLORS.BLUE
}

export function compareArrays(arrayA: Array<unknown>, arrayB: Array<unknown>) {
    if (arrayA.length != arrayB.length) return false
    for (let i = 0; i < arrayA.length; i++) {
        if (arrayA[i] != arrayB[i]) return false
    }
    return true
}